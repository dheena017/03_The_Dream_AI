import requests
from urllib.parse import quote_plus
from typing import List, Dict, Optional

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    BeautifulSoup = None  # Optional dependency; code will guard usage


class WebResearcher:
    """Lightweight web research helper with safe fallbacks.

    - DuckDuckGo HTML search parsing (no API key required)
    - JSON/text fetch helpers with timeouts
    """

    def __init__(self, user_agent: Optional[str] = None, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": user_agent
            or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        }

    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Perform a simple DuckDuckGo search and return top results.

        Returns a list of dicts: {title, url, snippet}
        Requires beautifulsoup4; if unavailable, returns empty list.
        """
        if BeautifulSoup is None:
            return []

        # Use the HTML endpoint to avoid JS
        url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            results: List[Dict[str, str]] = []
            # DuckDuckGo HTML results are in div.result or similar; be tolerant
            for res in soup.select("div.result, div.web-result, div.result__body"):
                a = res.select_one("a.result__a, a[href]")
                if not a or not a.get("href"):
                    continue
                title = a.get_text(strip=True)
                href = a.get("href")
                snippet_el = res.select_one("a.result__snippet, div.result__snippet, .snippet")
                snippet = snippet_el.get_text(strip=True) if snippet_el else ""
                results.append({"title": title, "url": href, "snippet": snippet})
                if len(results) >= max_results:
                    break

            return results
        except Exception:
            return []

    def fetch_json(self, url: str, params: Optional[dict] = None) -> Optional[dict]:
        try:
            r = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    def fetch_text(self, url: str, max_len: int = 5000) -> Optional[str]:
        try:
            r = requests.get(url, headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
            text = r.text
            if len(text) > max_len:
                return text[: max_len] + "\n... [truncated]"
            return text
        except Exception:
            return None
