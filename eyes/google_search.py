"""
GOOGLE SEARCH MODULE
Enables Eyes to search the internet using Google Search API
Provides web search capabilities for the Brain to learn from the web
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import urllib.parse


class GoogleSearchCapability:
    """Enable internet search functionality for Eyes"""
    
    def __init__(self, api_key: str = None, search_engine_id: str = None):
        """
        Initialize Google Search capability
        
        To get API credentials:
        1. Go to Google Cloud Console: https://console.cloud.google.com/
        2. Create a new project
        3. Enable Custom Search API
        4. Create API key
        5. Set up Custom Search Engine: https://programmablesearchengine.google.com/
        6. Get search engine ID
        
        For development: Can use DuckDuckGo as fallback (no API key needed)
        """
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.google_search_url = "https://www.googleapis.com/customsearch/v1"
        self.duckduckgo_url = "https://duckduckgo.com/api"
        self.search_history: List[Dict] = []
        self.is_available = bool(api_key and search_engine_id)
    
    def search(self, query: str, max_results: int = 5, use_fallback: bool = True) -> List[Dict]:
        """
        Search the internet for a query
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            use_fallback: Use DuckDuckGo if Google API unavailable
            
        Returns:
            List of search results with title, url, snippet
        """
        results = []
        
        # Try Google Search API first
        if self.is_available:
            results = self._google_search(query, max_results)
        
        # Fallback to DuckDuckGo if no results or API unavailable
        if not results and use_fallback:
            results = self._duckduckgo_search(query, max_results)
        
        # Store in history
        self.search_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "result_count": len(results)
        })
        
        return results
    
    def _google_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using Google Custom Search API"""
        try:
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": query,
                "num": min(max_results, 10),
                "safe": "active"
            }
            
            response = requests.get(self.google_search_url, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️  Google Search API error: {response.status_code}")
                return []
            
            data = response.json()
            items = data.get("items", [])
            
            results = []
            for item in items[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "google",
                    "timestamp": datetime.now().isoformat()
                })
            
            return results
        
        except Exception as e:
            print(f"⚠️  Google Search error: {e}")
            return []
    
    def _duckduckgo_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using DuckDuckGo (no API key needed)"""
        try:
            # DuckDuckGo instant answer endpoint
            params = {
                "q": query,
                "format": "json",
                "no_redirect": 1,
                "no_html": 1,
                "skip_disambig": 1
            }
            
            headers = {
                "User-Agent": "Dream AI Eyes System"
            }
            
            response = requests.get(self.duckduckgo_url, params=params, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return self._fallback_web_search(query, max_results)
            
            data = response.json()
            results = []
            
            # Check for related topics (search results)
            related = data.get("Related", [])
            
            for item in related[:max_results]:
                results.append({
                    "title": item.get("FirstURL", "").split("/")[2] if item.get("FirstURL") else "Result",
                    "url": item.get("FirstURL", ""),
                    "snippet": item.get("Text", ""),
                    "source": "duckduckgo",
                    "timestamp": datetime.now().isoformat()
                })
            
            # If no related results, try alternative approach
            if not results:
                return self._fallback_web_search(query, max_results)
            
            return results
        
        except Exception as e:
            print(f"⚠️  DuckDuckGo search error: {e}")
            return self._fallback_web_search(query, max_results)
    
    def _fallback_web_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Fallback: Use requests to fetch from web search URL"""
        try:
            # Using Bing search as fallback (public accessible)
            search_url = f"https://www.bing.com/search"
            params = {"q": query}
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse HTML to extract results (simplified)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                results = []
                for item in soup.find_all('h2')[:max_results]:
                    link = item.find('a')
                    if link:
                        results.append({
                            "title": link.get_text(),
                            "url": link.get('href', ''),
                            "snippet": "Web search result",
                            "source": "bing",
                            "timestamp": datetime.now().isoformat()
                        })
                
                return results
        except Exception as e:
            print(f"⚠️  Fallback web search error: {e}")
        
        return []
    
    def search_by_type(self, query: str, search_type: str = "general") -> List[Dict]:
        """
        Search with specific type
        
        Types:
        - general: Regular web search
        - news: News articles
        - scholar: Academic papers
        - images: Images
        """
        if search_type == "general":
            return self.search(query)
        
        elif search_type == "news":
            return self._search_news(query)
        
        else:
            return self.search(query)
    
    def _search_news(self, query: str) -> List[Dict]:
        """Search news specifically"""
        try:
            # Using News API format (fallback to regular search)
            params = {
                "q": query,
                "sort_by": "publishedAt"
            }
            results = self.search(query, 5)
            for r in results:
                r["type"] = "news"
            return results
        except:
            return self.search(query)
    
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """Get search history"""
        return self.search_history[-limit:]
    
    def clear_search_history(self):
        """Clear search history"""
        self.search_history = []
    
    def get_status(self) -> Dict:
        """Get status of search capability"""
        return {
            "available": self.is_available,
            "provider": "google" if self.is_available else "duckduckgo/fallback",
            "total_searches": len(self.search_history),
            "fallback_enabled": True
        }


if __name__ == "__main__":
    # Test without API key (uses DuckDuckGo)
    search = GoogleSearchCapability()
    
    print("🔍 Google Search Capability Test")
    print(f"Status: {search.get_status()}")
    
    # Test search
    results = search.search("Python machine learning libraries")
    
    print(f"\n📊 Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet'][:100]}...")
        print(f"   Source: {result['source']}")
