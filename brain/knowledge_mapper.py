"""
KNOWLEDGE MAPPER
Maps your learning domains and knowledge acquisition patterns
"""

import datetime
from typing import Dict, List, Set
from collections import defaultdict, Counter

try:
    from .observation_memory import ObservationMemory
except ImportError:
    from observation_memory import ObservationMemory


class KnowledgeMapper:
    """Maps your knowledge domains and learning patterns"""
    
    def __init__(self, memory: ObservationMemory):
        self.memory = memory
    
    def identify_research_topics(self, hours: int = 24*7) -> Dict:
        """
        Identify what topics you research
        Based on browser history and search patterns
        """
        observations = self.memory.get_observations(limit=1000, hours=hours)
        
        topics = defaultdict(int)
        domains = Counter()
        keywords = Counter()
        
        for obs in observations:
            browser = obs.get("sensors", {}).get("browser", {})
            
            # Analyze browsing patterns
            for visit in browser.get("recent_visits", []):
                domain = visit.get("browser", "")
                title = visit.get("title", "").lower()
                url = visit.get("url", "").lower()
                
                if domain:
                    domains[domain] += 1
                
                # Extract keywords from title
                words = title.split()
                for word in words:
                    if len(word) > 4 and not word.startswith("http"):
                        keywords[word] += 1
            
            # Analyze patterns
            patterns = browser.get("browsing_patterns", {})
            for domain, data in patterns.get("top_domains", []):
                topics[domain] += 1
        
        return {
            "research_domains": domains.most_common(20),
            "top_keywords": keywords.most_common(30),
            "research_intensity": self._calculate_research_intensity(hours),
            "learning_areas": self._categorize_knowledge_areas(keywords.most_common(30))
        }
    
    def _calculate_research_intensity(self, hours: int) -> Dict:
        """Calculate how intensively you research"""
        observations = self.memory.get_observations(limit=1000, hours=hours)
        
        browser_time = 0
        coding_time = 0
        
        for obs in observations:
            screen = obs.get("sensors", {}).get("screen", {})
            app = screen.get("active_window", {}).get("app_name", "").lower()
            
            if any(x in app for x in ["firefox", "chrome", "browser"]):
                browser_time += 1
            elif any(x in app for x in ["code", "vim", "python", "editor"]):
                coding_time += 1
        
        total = browser_time + coding_time
        if total == 0:
            return {"research_ratio": 0, "learning_vs_building": "No data"}
        
        ratio = browser_time / total
        
        if ratio > 0.6:
            status = "Learning Heavy"
        elif ratio > 0.4:
            status = "Balanced"
        else:
            status = "Building Focus"
        
        return {
            "research_ratio": round(ratio, 2),
            "research_to_building": status,
            "browser_observations": browser_time,
            "coding_observations": coding_time
        }
    
    def _categorize_knowledge_areas(self, keywords: List[tuple]) -> List[str]:
        """Categorize research keywords into knowledge areas"""
        categories = {
            "Web Development": ["javascript", "react", "vue", "html", "css", "node"],
            "Python": ["python", "django", "flask", "numpy", "pandas"],
            "Data Science": ["machine learning", "data analysis", "statistics", "ai"],
            "DevOps": ["docker", "kubernetes", "deployment", "ci/cd"],
            "Mobile": ["react native", "flutter", "ios", "android"],
            "Databases": ["sql", "mongodb", "postgres", "database"],
            "Testing": ["testing", "unit test", "jest", "pytest"],
            "Architecture": ["design patterns", "microservices", "architecture"]
        }
        
        discovered_areas = set()
        keyword_set = {kw for kw, _ in keywords}
        
        for category, keywords_in_cat in categories.items():
            if any(kw in keyword_set or any(k in kw for k in keywords_in_cat) 
                   for kw in keyword_set):
                discovered_areas.add(category)
        
        return list(discovered_areas)
    
    def map_knowledge_graph(self) -> Dict:
        """
        Create a knowledge graph of connections between topics
        - What concepts you learn together
        - Prerequisites you research before coding
        """
        observations = self.memory.get_observations(limit=1000, hours=24*7)
        
        connections = defaultdict(lambda: defaultdict(int))
        
        # Track what apps/sites are used together
        for obs in observations:
            screen = obs.get("sensors", {}).get("screen", {})
            app = screen.get("active_window", {}).get("app_name", "").lower()
            
            browser = obs.get("sensors", {}).get("browser", {})
            if browser.get("recent_visits"):
                visit = browser["recent_visits"][0]
                domain = visit.get("browser", "")
                
                if app and domain:
                    connections[app][domain] += 1
        
        return {
            "tool_connections": dict(connections),
            "knowledge_correlation": "Analyzing..."
        }
    
    def identify_learning_style(self) -> Dict:
        """
        Identify your learning style based on patterns
        - Video learner?
        - Tutorial reader?
        - Documentation browser?
        - Hands-on coder?
        """
        observations = self.memory.get_observations(limit=1000, hours=24*7)
        
        behaviors = {
            "video_consumption": 0,
            "documentation_reading": 0,
            "hands_on_coding": 0,
            "searching": 0
        }
        
        for obs in observations:
            browser = obs.get("sensors", {}).get("browser", {})
            for visit in browser.get("recent_visits", []):
                title = visit.get("title", "").lower()
                url = visit.get("url", "").lower()
                
                if any(x in url for x in ["youtube", "vimeo", "skillshare"]):
                    behaviors["video_consumption"] += 1
                elif any(x in url for x in ["docs", "documentation", "tutorial"]):
                    behaviors["documentation_reading"] += 1
                elif any(x in url for x in ["github", "stackoverflow", "example"]):
                    behaviors["hands_on_coding"] += 1
                elif any(x in url for x in ["google", "search", "find"]):
                    behaviors["searching"] += 1
        
        total = sum(behaviors.values())
        if total == 0:
            return {"style": "Insufficient data"}
        
        percentages = {k: round(v/total*100, 1) for k, v in behaviors.items()}
        
        primary_style = max(behaviors.items(), key=lambda x: x[1])[0]
        
        return {
            "primary_style": primary_style,
            "behavior_breakdown": percentages,
            "description": self._describe_learning_style(primary_style)
        }
    
    def _describe_learning_style(self, style: str) -> str:
        """Describe learning style"""
        descriptions = {
            "video_consumption": "Visual learner - prefers video tutorials and demonstrations",
            "documentation_reading": "Detail-oriented learner - reads comprehensive documentation",
            "hands_on_coding": "Practical learner - learns by building and experimenting",
            "searching": "Problem-solver learner - searches for solutions to specific issues"
        }
        return descriptions.get(style, "Balanced learner")
    
    def get_knowledge_map_report(self) -> Dict:
        """Complete knowledge mapping report"""
        return {
            "research_topics": self.identify_research_topics(),
            "knowledge_graph": self.map_knowledge_graph(),
            "learning_style": self.identify_learning_style(),
            "learning_velocity": self._calculate_learning_velocity(),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def _calculate_learning_velocity(self) -> Dict:
        """
        How fast are you learning?
        Based on diversity of topics and consistency
        """
        research = self.identify_research_topics()
        
        num_unique_domains = len(research["research_domains"])
        num_keywords = len(research["top_keywords"])
        
        velocity = min(10, (num_unique_domains + num_keywords) / 5)
        
        if velocity > 8:
            status = "Very Fast 🚀"
        elif velocity > 6:
            status = "Fast 📈"
        elif velocity > 4:
            status = "Steady 📊"
        else:
            status = "Slower pace 🐢"
        
        return {
            "velocity_score": round(velocity, 1),
            "status": status,
            "unique_domains_explored": num_unique_domains,
            "learning_breadth": num_keywords
        }


if __name__ == "__main__":
    memory = ObservationMemory()
    mapper = KnowledgeMapper(memory)
    
    print("🗺️  Knowledge Mapper")
    print("\nResearch Topics:")
    topics = mapper.identify_research_topics()
    print(f"  Top Domains: {topics['research_domains'][:3]}")
    
    print("\nLearning Style:")
    style = mapper.identify_learning_style()
    print(f"  Primary: {style.get('primary_style', 'Unknown')}")
    print(f"  Description: {style.get('description', 'N/A')}")


# 🧬 EVOLVED BY DREAM AI - Analysis: 28 complexity score
