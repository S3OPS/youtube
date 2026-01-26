"""
Standalone CLI Script for Automated YouTube Content Creation
Run this script to create and upload a video immediately
"""

import os
import sys
from dotenv import load_dotenv
from automation_engine import AutomationEngine


def main():
    """Main function to run the automation"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   Automated YouTube Content Creation System                 ║
    ║   with Amazon Affiliate Links                               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY', 'AMAZON_AFFILIATE_TAG']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file based on .env.example")
        sys.exit(1)
    
    # Initialize configuration
    config = {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'amazon_affiliate_tag': os.getenv('AMAZON_AFFILIATE_TAG', 'youraffid-20'),
        'content_topic': os.getenv('CONTENT_TOPIC', 'technology'),
        'content_frequency': os.getenv('CONTENT_FREQUENCY', 'daily'),
        'video_output_dir': 'generated_videos',
        'youtube_client_secrets': 'client_secrets.json',
        'video_privacy': os.getenv('VIDEO_PRIVACY', 'public')
    }
    
    print(f"📝 Configuration:")
    print(f"   Topic: {config['content_topic']}")
    print(f"   Frequency: {config['content_frequency']}")
    print(f"   Privacy: {config['video_privacy']}")
    print()
    
    # Initialize automation engine
    automation = AutomationEngine(config)
    
    # Create and upload video
    result = automation.create_and_upload_video()
    
    # Print summary
    print("\n" + "="*60)
    if result.get('status') == 'success':
        print("✅ SUCCESS!")
        print(f"   Title: {result.get('title')}")
        print(f"   Video URL: {result.get('video_url')}")
        print(f"   Video File: {result.get('video_file')}")
    else:
        print("❌ FAILED")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    print("="*60)


if __name__ == '__main__':
    main()
