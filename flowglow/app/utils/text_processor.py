from typing import Dict, List, Optional
from app.core.models import ContentRequest, ContentResponse, Platform
import re

class TextProcessor:
    """Utility class for text processing and content formatting"""
    
    @staticmethod
    def format_for_platform(content: str, platform: Platform) -> str:
        """Format content according to platform requirements"""
        formatters = {
            Platform.TWITTER: TextProcessor._format_for_twitter,
            Platform.INSTAGRAM: TextProcessor._format_for_instagram,
            Platform.LINKEDIN: TextProcessor._format_for_linkedin,
            Platform.BLOG: TextProcessor._format_for_blog
        }
        
        formatter = formatters.get(platform, lambda x: x)
        return formatter(content)
    
    @staticmethod
    def _format_for_twitter(content: str) -> str:
        """Format content for Twitter, including thread creation"""
        # Split into tweets if necessary
        max_length = 280
        tweets = []
        words = content.split()
        current_tweet = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_tweet.append(word)
                current_length += len(word) + 1
            else:
                tweets.append(" ".join(current_tweet))
                current_tweet = [word]
                current_length = len(word)
                
        if current_tweet:
            tweets.append(" ".join(current_tweet))
            
        # Add thread numbering if needed
        if len(tweets) > 1:
            return "\n\n".join(f"{i+1}/{len(tweets)} {tweet}" 
                             for i, tweet in enumerate(tweets))
        return tweets[0]
    
    @staticmethod
    def _format_for_instagram(content: str) -> str:
        """Format content for Instagram, including hashtag optimization"""
        # Extract and format hashtags
        hashtags = TextProcessor._extract_hashtags(content)
        main_content = TextProcessor._remove_hashtags(content)
        
        # Format with Instagram line breaks and emoji
        formatted_content = main_content.strip()
        if hashtags:
            formatted_content += "\n\n.\n.\n.\n" + " ".join(hashtags)
        
        return formatted_content
    
    @staticmethod
    def _format_for_linkedin(content: str) -> str:
        """Format content for LinkedIn, including professional styling"""
        # Add professional formatting
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for p in paragraphs:
            # Add bullet points for lists
            if any(line.strip().startswith('-') for line in p.split('\n')):
                formatted_paragraphs.append(p)
            else:
                formatted_paragraphs.append(p)
                
        return "\n\n".join(formatted_paragraphs)
    
    @staticmethod
    def _format_for_blog(content: str) -> str:
        """Format content for blog posts, including HTML conversion"""
        # Convert markdown-style formatting to HTML
        html_content = content
        # Convert headers
        html_content = re.sub(r'## (.*?)\n', r'<h2>\1</h2>\n', html_content)
        html_content = re.sub(r'# (.*?)\n', r'<h1>\1</h1>\n', html_content)
        
        # Convert paragraphs
        html_content = re.sub(r'\n\n(.*?)\n\n', r'\n<p>\1</p>\n', html_content)
        
        return html_content
    
    @staticmethod
    def _extract_hashtags(content: str) -> List[str]:
        """Extract hashtags from content"""
        return re.findall(r'#\w+', content)
    
    @staticmethod
    def _remove_hashtags(content: str) -> str:
        """Remove hashtags from main content"""
        return re.sub(r'#\w+\s*', '', content).strip()