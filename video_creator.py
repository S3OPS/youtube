"""
Video Creator Module
Creates videos from scripts using text-to-speech and stock footage
"""

import os
from gtts import gTTS
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip, 
    concatenate_videoclips, TextClip, ColorClip
)
from PIL import Image, ImageDraw, ImageFont
import random
from datetime import datetime


class VideoCreator:
    def __init__(self, output_dir="generated_videos"):
        """Initialize the video creator"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs("temp", exist_ok=True)
    
    def text_to_speech(self, text, output_file=None):
        """Convert text to speech using gTTS"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"temp/audio_{timestamp}.mp3"
        
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
            # Random gradient colors
            colors = [
                [(41, 128, 185), (52, 152, 219)],  # Blue gradient
                [(142, 68, 173), (155, 89, 182)],  # Purple gradient
                [(39, 174, 96), (46, 204, 113)],   # Green gradient
                [(230, 126, 34), (241, 148, 138)], # Orange gradient
            ]
            color = random.choice(colors)
        
        img = Image.new('RGB', (width, height), color[0])
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for i in range(height):
            ratio = i / height
            r = int(color[0][0] * (1 - ratio) + color[1][0] * ratio)
            g = int(color[0][1] * (1 - ratio) + color[1][1] * ratio)
            b = int(color[0][2] * (1 - ratio) + color[1][2] * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"temp/background_{timestamp}.png"
        img.save(output_file)
        return output_file
    
    def create_video_from_script(self, script, title, output_file=None):
        """Create a video from a script"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{self.output_dir}/video_{timestamp}.mp4"
        
        try:
            # Create audio from script
            print("Generating audio...")
            audio_file = self.text_to_speech(script)
            if not audio_file:
                return None
            
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_file)
            duration = audio_clip.duration
            
            # Create background image
            print("Creating background...")
            bg_image_file = self.create_background_image()
            
            # Create video clip from image
            image_clip = ImageClip(bg_image_file).set_duration(duration)
            
            # Add title text
            print("Adding title...")
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
                
                # Composite video and text
                video = CompositeVideoClip([image_clip, title_clip])
            except Exception as e:
                print(f"Text overlay error: {e}, using image only")
                video = image_clip
            
            # Add audio to video
            final_video = video.set_audio(audio_clip)
            
            # Write the video file
            print(f"Rendering video to {output_file}...")
            final_video.write_videofile(
                output_file,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=f'temp/temp_audio_{datetime.now().strftime("%Y%m%d_%H%M%S")}.m4a',
                remove_temp=True
            )
            
            # Clean up
            audio_clip.close()
            final_video.close()
            
            # Remove temp files
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(bg_image_file):
                os.remove(bg_image_file)
            
            print(f"Video created successfully: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
    
    def create_simple_video(self, script, title):
        """Simplified video creation with basic visuals"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.output_dir}/video_{timestamp}.mp4"
        
        try:
            # Create audio
            print("Generating audio...")
            audio_file = self.text_to_speech(script)
            if not audio_file:
                return None
            
            audio_clip = AudioFileClip(audio_file)
            duration = audio_clip.duration
            
            # Create a simple colored background
            print("Creating background...")
            video = ColorClip(
                size=(1920, 1080),
                color=(41, 128, 185),
                duration=duration
            )
            
            # Add audio
            final_video = video.set_audio(audio_clip)
            
            # Write video
            print(f"Rendering video to {output_file}...")
            final_video.write_videofile(
                output_file,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Clean up
            audio_clip.close()
            final_video.close()
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            print(f"Video created successfully: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
