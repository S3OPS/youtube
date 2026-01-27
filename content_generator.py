"""
Content Generator Module
Generates video scripts and content using AI
"""

import openai
import os
import json
import random
from functools import lru_cache
from utils import get_timestamp_string, validate_api_key
from config import Config
from cache import SimpleCache


class ContentGenerator:
    def __init__(self, api_key, topic="technology", model=None, enable_cache=True):
        """Initialize the content generator with OpenAI API key"""
        self.api_key = validate_api_key(api_key, "OpenAI API key")
        self.client = openai.OpenAI(api_key=self.api_key)
        self.topic = topic
        self.model = model or Config.DEFAULT_MODEL
        # Initialize cache (1 hour TTL for API responses)
        self.cache = SimpleCache(cache_dir='.cache/content_gen', ttl_seconds=3600) if enable_cache else None
        
    def _call_openai_api(self, system_prompt, user_prompt, max_tokens, temperature=0.7):
        """Centralized OpenAI API call with error handling and caching
        
        Args:
            system_prompt: System role content
            user_prompt: User message content
            max_tokens: Maximum tokens for response
            temperature: Sampling temperature
            
        Returns:
            API response content or None on error
        """
        # Check cache if enabled
        if self.cache:
            cache_key = self.cache.get_cache_key(
                self.model, system_prompt, user_prompt, max_tokens, temperature
            )
            cached_response = self.cache.get(cache_key)
            if cached_response:
                print("Using cached API response")
                return cached_response
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            result = response.choices[0].message.content.strip()
            
            # Cache the response
            if self.cache and result:
                self.cache.set(cache_key, result)
            
            return result
        except openai.APIError as e:
            print(f"OpenAI API error: {e}")
            return None
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
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
        
        script = self._call_openai_api(
            system_prompt="You are a professional YouTube content creator.",
            user_prompt=prompt,
            max_tokens=Config.DEFAULT_MAX_TOKENS_SCRIPT,
            temperature=0.8
        )
        
        return script if script else self._get_fallback_script()
    
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
        
        result_str = self._call_openai_api(
            system_prompt="You are a YouTube SEO expert.",
            user_prompt=prompt,
            max_tokens=Config.DEFAULT_MAX_TOKENS_METADATA,
            temperature=0.7
        )
        
        if not result_str:
            return "Amazing Content", script[:500] if script else "Check out this video!"
        
        try:
            result = json.loads(result_str)
            return result.get('title', 'Amazing Video'), result.get('description', script[:500])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return "Amazing Content", script[:500] if script else "Check out this video!"
    
    def generate_product_keywords(self, script):
        """Extract product keywords for Amazon affiliate links"""
        prompt = f"""Based on this video script, suggest 3-5 Amazon products that would be relevant
        and useful for viewers. Return only product search keywords, one per line.
        
        Script:
        {script}
        
        Return as a simple list, one keyword per line."""
        
        keywords_str = self._call_openai_api(
            system_prompt="You are an e-commerce product expert.",
            user_prompt=prompt,
            max_tokens=Config.DEFAULT_MAX_TOKENS_KEYWORDS,
            temperature=0.6
        )
        
        if not keywords_str:
            return ["tech gadgets", "electronics", "accessories"]
        
        try:
            keywords = keywords_str.strip().split('\n')
            return [k.strip().strip('-').strip('•').strip() for k in keywords if k.strip()][:5]
        except Exception as e:
            print(f"Error parsing keywords: {e}")
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
            timestamp = get_timestamp_string()
            filename = f"generated_scripts/script_{timestamp}.txt"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script)
        
        return filename
