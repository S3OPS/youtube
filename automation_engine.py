"""
Automation Engine
Coordinates content generation, video creation, and YouTube upload
"""

import os
import json
from datetime import datetime
import schedule
import time
from content_generator import ContentGenerator
from amazon_affiliate import AmazonAffiliate
from video_creator import VideoCreator
from youtube_uploader import YouTubeUploader
from utils import load_json_file, save_json_file


class AutomationEngine:
    def __init__(self, config):
        """Initialize the automation engine with configuration"""
        self.config = config
        
        # Initialize components
        self.content_gen = ContentGenerator(
            api_key=config.get('openai_api_key'),
            topic=config.get('content_topic', 'technology')
        )
        
        self.amazon_affiliate = AmazonAffiliate(
            affiliate_tag=config.get('amazon_affiliate_tag')
        )
        
        self.video_creator = VideoCreator(
            output_dir=config.get('video_output_dir', 'generated_videos')
        )
        
        self.youtube_uploader = YouTubeUploader(
            client_secrets_file=config.get('youtube_client_secrets', 'client_secrets.json')
        )
        
        self.history = []
        self.history_file = 'automation_history.json'
        self._load_history()
    
    def _load_history(self):
        """Load automation history from file"""
        self.history = load_json_file(self.history_file, default=[])
        if not self.history:
            print(f"No existing history found or failed to load from {self.history_file}")
    
    def _save_history(self):
        """Save automation history to file"""
        save_json_file(self.history_file, self.history)
    
    def _generate_content(self, entry):
        """Generate script, title, description, and keywords
        
        Args:
            entry: Dictionary to populate with generated content
            
        Returns:
            Tuple of (script, title, description_with_links, keywords) or (None, ...) on error
        """
        # Step 1: Generate script
        print("Step 1: Generating video script...")
        script = self.content_gen.generate_video_script()
        if not script:
            raise Exception("Failed to generate script")
        print(f"Script generated ({len(script)} characters)")
        entry['script_length'] = len(script)
        
        # Save script
        script_file = self.content_gen.save_script(script)
        entry['script_file'] = script_file
        
        # Step 2: Generate title and description
        print("\nStep 2: Generating title and description...")
        title, description = self.content_gen.generate_title_and_description(script)
        print(f"Title: {title}")
        entry['title'] = title
        
        # Step 3: Generate product keywords for affiliate links
        print("\nStep 3: Generating Amazon affiliate links...")
        keywords = self.content_gen.generate_product_keywords(script)
        print(f"Keywords: {', '.join(keywords)}")
        entry['keywords'] = keywords
        
        # Add affiliate links to description
        description_with_links = self.amazon_affiliate.format_description_with_links(
            description, keywords
        )
        entry['description'] = description_with_links
        
        return script, title, description_with_links, keywords
    
    def _create_video_file(self, script, title, entry):
        """Create video file from script
        
        Args:
            script: Video script text
            title: Video title
            entry: Dictionary to populate with video info
            
        Returns:
            Path to created video file or None on error
        """
        print("\nStep 4: Creating video...")
        video_file = self.video_creator.create_simple_video(script, title)
        if not video_file:
            raise Exception("Video creation failed - video_creator.create_simple_video returned None")
        print(f"Video created: {video_file}")
        entry['video_file'] = video_file
        return video_file
    
    def _upload_to_youtube(self, video_file, title, description, keywords, entry):
        """Upload video to YouTube
        
        Args:
            video_file: Path to video file
            title: Video title
            description: Video description
            keywords: List of keywords/tags
            entry: Dictionary to populate with upload info
            
        Returns:
            Video ID on success, None on error
        """
        print("\nStep 5: Uploading to YouTube...")
        video_id = self.youtube_uploader.upload_video(
            video_file=video_file,
            title=title,
            description=description,
            tags=keywords,
            privacy_status=self.config.get('video_privacy', 'public')
        )
        
        if video_id:
            entry['video_id'] = video_id
            entry['video_url'] = f"https://www.youtube.com/watch?v={video_id}"
            print(f"\n✓ Success! Video uploaded: {entry['video_url']}")
            return video_id
        else:
            print("\n✗ Failed to upload video")
            return None
    
    def _record_history(self, entry):
        """Record the automation run in history
        
        Args:
            entry: Dictionary containing automation run details
        """
        self.history.append(entry)
        self._save_history()
    
    def create_and_upload_video(self):
        """Complete workflow: generate content, create video, upload to YouTube"""
        print(f"\n{'='*60}")
        print(f"Starting automated content creation - {datetime.now()}")
        print(f"{'='*60}\n")
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'status': 'started'
        }
        
        try:
            # Generate content
            script, title, description, keywords = self._generate_content(entry)
            
            # Create video
            video_file = self._create_video_file(script, title, entry)
            
            # Upload to YouTube
            video_id = self._upload_to_youtube(video_file, title, description, keywords, entry)
            
            # Set final status
            if video_id:
                entry['status'] = 'success'
            else:
                entry['status'] = 'upload_failed'
            
        except Exception as e:
            entry['status'] = 'failed'
            entry['error'] = str(e)
            print(f"\n✗ Error: {e}")
        
        # Save to history
        self._record_history(entry)
        
        print(f"\n{'='*60}")
        print(f"Completed - {datetime.now()}")
        print(f"{'='*60}\n")
        
        return entry
    
    def get_status(self):
        """Get current automation status"""
        return {
            'total_videos': len(self.history),
            'successful': len([h for h in self.history if h.get('status') == 'success']),
            'failed': len([h for h in self.history if h.get('status') == 'failed']),
            'last_run': self.history[-1] if self.history else None,
            'config': {
                'topic': self.config.get('content_topic'),
                'frequency': self.config.get('content_frequency')
            }
        }
    
    def schedule_automation(self, frequency='daily'):
        """Schedule automatic content creation"""
        print(f"Scheduling automation: {frequency}")
        
        if frequency == 'hourly':
            schedule.every().hour.do(self.create_and_upload_video)
        elif frequency == 'daily':
            schedule.every().day.at("09:00").do(self.create_and_upload_video)
        elif frequency == 'weekly':
            schedule.every().monday.at("09:00").do(self.create_and_upload_video)
        
        print("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nScheduler stopped.")
