"""
Amazon Affiliate Link Generator
Generates Amazon affiliate links for products
"""

import urllib.parse


class AmazonAffiliate:
    def __init__(self, affiliate_tag):
        """Initialize with Amazon affiliate tag"""
        self.affiliate_tag = affiliate_tag
        self.base_url = "https://www.amazon.com/s"
    
    def generate_search_link(self, keyword):
        """Generate an Amazon affiliate search link for a keyword"""
        params = {
            'k': keyword,
            'tag': self.affiliate_tag
        }
        query_string = urllib.parse.urlencode(params)
        return f"{self.base_url}?{query_string}"
    
    def generate_product_link(self, asin):
        """Generate an Amazon affiliate product link using ASIN"""
        return f"https://www.amazon.com/dp/{asin}?tag={self.affiliate_tag}"
    
    def format_description_with_links(self, description, keywords):
        """Add affiliate links to video description"""
        links_section = "\n\n🛒 RECOMMENDED PRODUCTS:\n"
        
        for i, keyword in enumerate(keywords, 1):
            link = self.generate_search_link(keyword)
            links_section += f"{i}. {keyword.title()}: {link}\n"
        
        links_section += "\n💡 As an Amazon Associate, I earn from qualifying purchases.\n"
        
        return description + links_section
    
    def create_pinned_comment(self, keywords):
        """Create a pinned comment with affiliate links"""
        comment = "🔥 PRODUCTS MENTIONED IN THIS VIDEO:\n\n"
        
        for i, keyword in enumerate(keywords, 1):
            link = self.generate_search_link(keyword)
            comment += f"{i}. {keyword.title()}\n   {link}\n\n"
        
        comment += "💡 These are affiliate links. Using them supports the channel at no extra cost to you. Thanks!"
        
        return comment
