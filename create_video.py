"""
Standalone CLI Script for Automated YouTube Content Creation
Run this script to create and upload a video immediately
"""

import os
import sys
import subprocess
import importlib.util
import shutil
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None
try:
    from automation_engine import AutomationEngine
except ModuleNotFoundError:
    AutomationEngine = None


def run_preflight_checks():
    """Run preflight checks for the full automation workflow."""
    print("Step 0: Running preflight checks...")
    errors = []

    if sys.version_info < (3, 8):
        errors.append(f"Python 3.8+ required (current: {sys.version.split()[0]})")

    required_modules = {
        'dotenv': 'python-dotenv',
        'openai': 'openai',
        'googleapiclient.discovery': 'google-api-python-client',
        'google.auth_oauthlib': 'google-auth-oauthlib',
        'google.auth_httplib2': 'google-auth-httplib2',
        'gtts': 'gtts',
        'moviepy': 'moviepy',
        'schedule': 'schedule',
        'requests': 'requests',
        'bs4': 'beautifulsoup4',
        'lxml': 'lxml',
        'PIL': 'pillow',
        'pyttsx3': 'pyttsx3'
    }
    missing_packages = []
    for module, package in required_modules.items():
        try:
            spec = importlib.util.find_spec(module)
        except ModuleNotFoundError:
            spec = None
        if spec is None:
            missing_packages.append(package)
    if missing_packages:
        errors.append(
            f"Missing Python packages: {', '.join(missing_packages)} "
            "(run: pip install -r requirements.txt)"
        )

    if AutomationEngine is None:
        errors.append("Automation engine unavailable (install dependencies and retry)")

    if not shutil.which('ffmpeg'):
        errors.append("ffmpeg is not installed (required for video rendering)")
    else:
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            errors.append("ffmpeg check failed (ensure ffmpeg runs from your PATH)")

    required_vars = ['OPENAI_API_KEY', 'AMAZON_AFFILIATE_TAG']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        errors.append(f"Missing required environment variables: {', '.join(missing_vars)}")

    if not os.path.exists('client_secrets.json'):
        errors.append("client_secrets.json not found (required for YouTube upload)")

    if errors:
        print("❌ Preflight checks failed:")
        for error in errors:
            print(f"   - {error}")
        print("\nResolve the issues above and try again.")
        return False

    print("✅ Preflight checks passed.\n")
    return True


def main():
    """Main function to run the automation"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   Automated YouTube Content Creation System                 ║
    ║   with Amazon Affiliate Links                               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Load environment variables
    if load_dotenv:
        load_dotenv()

    if not run_preflight_checks():
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
