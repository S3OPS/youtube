"""
Content Generator Module
Generates video scripts and content using AI
"""

import openai
import os
from datetime import datetime
import json
import random


class ContentGenerator:
    def __init__(self, api_key, topic="technology"):
        """Initialize the content generator with OpenAI API key"""
        self.api_key = api_key
        openai.api_key = api_key
        self.topic = topic
        
    def generate_video_script(self, topic=None):
        """Generate a video script using AI"""
        if topic is None:
            topic = self.topic
            
        prompt = f"""Create an engaging, informative YouTube video script about {topic}.
        
        The script should:
        - Be 60 seconds long when spoken
        - Start with a hook to grab attention
        - Include 3-5 key points
        - End with a call to action
        - Be conversational and engaging
        - Include natural pauses for visuals
        
        Format the script as spoken narration only, no stage directions."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional YouTube content creator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            script = response.choices[0].message.content.strip()
            return script
        except Exception as e:
            print(f"Error generating script: {e}")
            return self._get_fallback_script()
    
    def generate_title_and_description(self, script):
        """Generate title and description based on the script"""
        prompt = f"""Based on this video script, create:
        1. A catchy, SEO-friendly YouTube title (max 60 characters)
        2. A comprehensive video description (2-3 paragraphs)
        
        Script:
        {script}
        
        Return in JSON format:
        {{
            "title": "...",
            "description": "..."
        }}"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a YouTube SEO expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result.get('title', 'Amazing Video'), result.get('description', script[:500])
        except Exception as e:
            print(f"Error generating title/description: {e}")
            return "Amazing Content", script[:500] if script else "Check out this video!"
    
    def generate_product_keywords(self, script):
        """Extract product keywords for Amazon affiliate links"""
        prompt = f"""Based on this video script, suggest 3-5 Amazon products that would be relevant
        and useful for viewers. Return only product search keywords, one per line.
        
        Script:
        {script}
        
        Return as a simple list, one keyword per line."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an e-commerce product expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.6
            )
            
            keywords = response.choices[0].message.content.strip().split('\n')
            return [k.strip().strip('-').strip('•').strip() for k in keywords if k.strip()][:5]
        except Exception as e:
            print(f"Error generating keywords: {e}")
            return ["tech gadgets", "electronics", "accessories"]
    
    def _get_fallback_script(self):
        """Fallback script when API fails"""
        return """Hey there! Today we're diving into an exciting topic that you won't want to miss. 
        First, we'll explore the fundamentals and why this matters to you. 
        Then, we'll look at some practical applications you can use right away. 
        Finally, we'll wrap up with actionable tips you can implement today. 
        Don't forget to like and subscribe for more great content!"""
    
    def save_script(self, script, filename=None):
        """Save the generated script to a file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_scripts/script_{timestamp}.txt"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script)
        
        return filename
