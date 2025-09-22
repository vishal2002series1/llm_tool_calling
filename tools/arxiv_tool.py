import requests
import xml.etree.ElementTree as ET

class ArxivTool:
    BASE_URL = "http://export.arxiv.org/api/query"

    @staticmethod
    def search(query, max_results=3):
        """
        Search Arxiv for papers matching the query.

        Returns: list of dicts with {title, summary, link, published}
        """
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results
        }

        response = requests.get(ArxivTool.BASE_URL, params=params)
        if response.status_code != 200:
            return [{"error": f"Failed to fetch from arXiv: {response.status_code}"}]

        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entries = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            link = entry.find("atom:id", ns).text.strip()
            published = entry.find("atom:published", ns).text.strip()

            entries.append({
                "title": title,
                "summary": summary,
                "link": link,
                "published": published
            })

        return entries