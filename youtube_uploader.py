"""
YouTube Uploader Module
Handles uploading videos to YouTube using YouTube Data API v3
"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from utils import get_secure_directory

# Import new infrastructure if available
try:
    from core.logging import get_logger
    from core.exceptions import AuthenticationError, UploadError
    from core.base import BaseAPIClient
    from core.file_utils import FileManager
    _HAS_CORE = True
except ImportError:
    _HAS_CORE = False


class YouTubeUploader:
    # Scopes required for YouTube upload
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
              'https://www.googleapis.com/auth/youtube.force-ssl']
    
    def __init__(self, client_secrets_file='client_secrets.json'):
        """Initialize YouTube uploader"""
        self.client_secrets_file = client_secrets_file
        self.youtube = None
        self.credentials = None
        # Store credentials in secure user directory
        if _HAS_CORE:
            self.creds_dir = FileManager.get_secure_user_directory('credentials')
            self.logger = get_logger(__name__)
        else:
            self.creds_dir = get_secure_directory('credentials')
            self.logger = None
        self.token_file = os.path.join(self.creds_dir, 'token.pickle')
    
    def _load_saved_credentials(self):
        """Load saved credentials from file"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'rb') as token:
                    return pickle.load(token)
            except Exception as e:
                msg = f"Error loading saved credentials: {e}"
                if self.logger:
                    self.logger.error(msg)
                else:
                    print(msg)
        return None
    
    def _save_credentials(self, credentials):
        """Save credentials to file"""
        try:
            with open(self.token_file, 'wb') as token:
                pickle.dump(credentials, token)
            return True
        except Exception as e:
            msg = f"Error saving credentials: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return False
    
    def _refresh_credentials(self, credentials):
        """Refresh expired credentials"""
        try:
            credentials.refresh(Request())
            return True
        except Exception as e:
            msg = f"Error refreshing credentials: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return False
    
    def _create_new_credentials(self):
        """Create new credentials via OAuth flow"""
        if not os.path.exists(self.client_secrets_file):
            msg = f"Error: {self.client_secrets_file} not found!"
            if self.logger:
                self.logger.error(msg)
                self.logger.error("Please download OAuth 2.0 credentials from Google Cloud Console")
            else:
                print(msg)
                print("Please download OAuth 2.0 credentials from Google Cloud Console")
            return None
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, self.SCOPES)
            return flow.run_local_server(port=0)
        except Exception as e:
            msg = f"Error creating new credentials: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return None
    
    def authenticate(self):
        """Authenticate with YouTube API"""
        # Load credentials from file if they exist
        self.credentials = self._load_saved_credentials()
        
        # If there are no valid credentials, let the user log in
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                if not self._refresh_credentials(self.credentials):
                    self.credentials = self._create_new_credentials()
            else:
                self.credentials = self._create_new_credentials()
            
            if not self.credentials:
                return False
            
            # Save credentials for future use
            self._save_credentials(self.credentials)
        
        # Build the YouTube service
        try:
            self.youtube = build('youtube', 'v3', credentials=self.credentials)
            return True
        except Exception as e:
            msg = f"Error building YouTube service: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return False
    
    def upload_video(self, video_file, title, description, category_id='22', 
                     privacy_status='public', tags=None, made_for_kids=False):
        """
        Upload a video to YouTube
        
        Args:
            video_file: Path to video file
            title: Video title
            description: Video description
            category_id: YouTube category ID (22 = People & Blogs)
            privacy_status: 'public', 'private', or 'unlisted'
            tags: List of tags for the video
            made_for_kids: Whether content is made for kids (COPPA compliance)
        
        Returns:
            Video ID if successful, None otherwise
        """
        if not self.youtube:
            if not self.authenticate():
                return None
        
        if tags is None:
            tags = []
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': made_for_kids
            }
        }
        
        # Create MediaFileUpload object with 1MB chunks for better progress tracking
        media = MediaFileUpload(
            video_file,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True,
            mimetype='video/mp4'
        )
        
        try:
            # Execute the upload
            msg = f"Uploading video: {title}"
            if self.logger:
                self.logger.info(msg)
            else:
                print(msg)
            
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress_msg = f"Upload progress: {int(status.progress() * 100)}%"
                    if self.logger:
                        self.logger.info(progress_msg)
                    else:
                        print(progress_msg)
            
            video_id = response['id']
            success_msg = f"Video uploaded successfully! Video ID: {video_id}"
            url_msg = f"Video URL: https://www.youtube.com/watch?v={video_id}"
            if self.logger:
                self.logger.info(success_msg)
                self.logger.info(url_msg)
            else:
                print(success_msg)
                print(url_msg)
            
            return video_id
            
        except HttpError as e:
            msg = f"HTTP error uploading video: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return None
        except Exception as e:
            msg = f"Error uploading video: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return None
    
    def update_video_description(self, video_id, new_description):
        """Update the description of an existing video"""
        if not self.youtube:
            if not self.authenticate():
                return False
        
        try:
            # Get current video details
            video_response = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                msg = f"Video {video_id} not found"
                if self.logger:
                    self.logger.error(msg)
                else:
                    print(msg)
                return False
            
            # Update the description
            video_snippet = video_response['items'][0]['snippet']
            video_snippet['description'] = new_description
            
            # Update the video
            self.youtube.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': video_snippet
                }
            ).execute()
            
            msg = "Video description updated successfully"
            if self.logger:
                self.logger.info(msg)
            else:
                print(msg)
            return True
            
        except HttpError as e:
            msg = f"HTTP error updating video: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return False
        except Exception as e:
            msg = f"Error updating video: {e}"
            if self.logger:
                self.logger.error(msg)
            else:
                print(msg)
            return False
