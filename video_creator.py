"""
Video Creator Module
Creates videos from scripts using text-to-speech and stock footage
"""

import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from gtts import gTTS
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip, 
    concatenate_videoclips, TextClip, ColorClip
)
from PIL import Image, ImageDraw, ImageFont
import random
from utils import get_timestamp_string


class VideoCreator:
    # Color schemes for backgrounds
    COLOR_SCHEMES = [
        [(41, 128, 185), (52, 152, 219)],  # Blue gradient
        [(142, 68, 173), (155, 89, 182)],  # Purple gradient
        [(39, 174, 96), (46, 204, 113)],   # Green gradient
        [(230, 126, 34), (241, 148, 138)], # Orange gradient
    ]
    
    def __init__(self, output_dir="generated_videos", max_workers=2):
        """Initialize the video creator
        
        Args:
            output_dir: Directory for output videos
            max_workers: Maximum parallel workers for batch processing
        """
        self.output_dir = output_dir
        self.max_workers = max_workers
        os.makedirs(output_dir, exist_ok=True)
        # Use secure temp directory
        self.temp_dir = tempfile.mkdtemp(prefix="youtube_video_", dir=tempfile.gettempdir())
        os.chmod(self.temp_dir, 0o700)
    
    def cleanup(self):
        """Clean up temporary directory"""
        import shutil
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"Warning: Could not remove temp directory {self.temp_dir}: {e}")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.cleanup()
    
    def text_to_speech(self, text, output_file=None):
        """Convert text to speech using gTTS"""
        if output_file is None:
            timestamp = get_timestamp_string()
            output_file = os.path.join(self.temp_dir, f"audio_{timestamp}.mp3")
        
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"Error creating audio: {e}")
            return None
    
    def create_background_image(self, width=1920, height=1080, color=None):
        """Create a simple background image"""
        if color is None:
            color = random.choice(self.COLOR_SCHEMES)
        
        img = Image.new('RGB', (width, height), color[0])
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for i in range(height):
            ratio = i / height
            r = int(color[0][0] * (1 - ratio) + color[1][0] * ratio)
            g = int(color[0][1] * (1 - ratio) + color[1][1] * ratio)
            b = int(color[0][2] * (1 - ratio) + color[1][2] * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        timestamp = get_timestamp_string()
        output_file = os.path.join(self.temp_dir, f"background_{timestamp}.png")
        img.save(output_file)
        return output_file
    
    def _create_audio_clip(self, script):
        """Create audio clip from script
        
        Returns:
            Tuple of (audio_clip, audio_file_path) or (None, None) on error
        """
        print("Generating audio...")
        audio_file = self.text_to_speech(script)
        if not audio_file:
            return None, None
        
        try:
            audio_clip = AudioFileClip(audio_file)
            return audio_clip, audio_file
        except Exception as e:
            print(f"Error loading audio: {e}")
            return None, None
    
    def _create_video_clip(self, duration, title=None, use_simple_bg=True):
        """Create video clip with background and optional title
        
        Args:
            duration: Video duration in seconds
            title: Optional title text to overlay
            use_simple_bg: If True, use solid color; if False, use gradient image
            
        Returns:
            Video clip or None on error
        """
        print("Creating background...")
        
        if use_simple_bg:
            # Simple solid color background
            video = ColorClip(
                size=(1920, 1080),
                color=(41, 128, 185),
                duration=duration
            )
        else:
            # Gradient background image
            bg_image_file = self.create_background_image()
            video = ImageClip(bg_image_file).set_duration(duration)
        
        # Add title if provided
        if title and not use_simple_bg:
            try:
                title_clip = TextClip(
                    title,
                    fontsize=70,
                    color='white',
                    font='Arial-Bold',
                    size=(1920, None),
                    method='caption',
                    align='center'
                ).set_position('center').set_duration(duration)
                
                video = CompositeVideoClip([video, title_clip])
            except Exception as e:
                print(f"Text overlay error: {e}, using background only")
        
        return video
    
    def _render_video(self, video_clip, output_file):
        """Render video clip to file with optimized settings
        
        Args:
            video_clip: MoviePy video clip
            output_file: Output file path
            
        Returns:
            True on success, False on error
        """
        try:
            print(f"Rendering video to {output_file}...")
            video_clip.write_videofile(
                output_file,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=os.path.join(self.temp_dir, f'temp_audio_{get_timestamp_string()}.m4a'),
                remove_temp=True,
                logger=None,  # Suppress verbose output
                threads=4,  # Use multiple threads for encoding
                preset='medium',  # Balance between speed and quality
                audio_bitrate='128k'
            )
            return True
        except Exception as e:
            print(f"Error rendering video: {e}")
            return False
    
    def _cleanup_temp_files(self, *file_paths):
        """Clean up temporary files"""
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Warning: Could not remove temp file {file_path}: {e}")
    
    def create_video(self, script, title, use_simple_bg=True, output_file=None):
        """Create a video from a script (unified method)
        
        Args:
            script: Video script text
            title: Video title
            use_simple_bg: If True, use simple solid background; if False, use gradient
            output_file: Optional output file path
            
        Returns:
            Output file path on success, None on error
        """
        if output_file is None:
            timestamp = get_timestamp_string()
            output_file = f"{self.output_dir}/video_{timestamp}.mp4"
        
        # Initialize all resources to None for proper cleanup
        audio_clip = None
        video_clip = None
        audio_file = None
        bg_file = None
        
        try:
            # Step 1: Create audio
            audio_clip, audio_file = self._create_audio_clip(script)
            if not audio_clip:
                return None
            
            duration = audio_clip.duration
            
            # Step 2: Create video with background
            video_clip = self._create_video_clip(duration, title if not use_simple_bg else None, use_simple_bg)
            if not video_clip:
                return None
            
            # Step 3: Combine video and audio
            final_video = video_clip.set_audio(audio_clip)
            
            # Step 4: Render to file
            if not self._render_video(final_video, output_file):
                return None
            
            print(f"Video created successfully: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
        finally:
            # Clean up resources
            if audio_clip:
                audio_clip.close()
            if video_clip:
                video_clip.close()
            # Clean up temp files
            self._cleanup_temp_files(audio_file)
    
    # Keep these methods for backward compatibility
    def create_video_from_script(self, script, title, output_file=None):
        """Create a video from a script with gradient background"""
        return self.create_video(script, title, use_simple_bg=False, output_file=output_file)
    
    def create_simple_video(self, script, title):
        """Create a simple video with solid color background"""
        return self.create_video(script, title, use_simple_bg=True)
    
    def create_videos_batch(self, video_specs, max_batch_size=10):
        """Create multiple videos in parallel (batch processing)
        
        Args:
            video_specs: List of dicts with keys: script, title, use_simple_bg, output_file
            max_batch_size: Maximum number of videos to process in one batch (default: 10)
            
        Returns:
            List of (video_spec, output_file_or_none) tuples
        """
        if len(video_specs) > max_batch_size:
            raise ValueError(f"Batch size {len(video_specs)} exceeds maximum {max_batch_size}")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_spec = {
                executor.submit(
                    self.create_video,
                    spec['script'],
                    spec['title'],
                    spec.get('use_simple_bg', True),
                    spec.get('output_file')
                ): spec
                for spec in video_specs
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_spec):
                spec = future_to_spec[future]
                try:
                    output_file = future.result()
                    results.append((spec, output_file))
                    if output_file:
                        print(f"Batch: Completed {spec['title']}")
                    else:
                        print(f"Batch: Failed {spec['title']}")
                except Exception as e:
                    print(f"Batch: Error processing {spec['title']}: {e}")
                    results.append((spec, None))
        
        return results
