# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from langdetect import detect

# Topic dictionary (copy your topic_sites here)
topic_sites = {
    "Politics": {
        "Telangana Politics": ["https://www.sakshi.com/news/telangana", "https://www.eenadu.net/telangana"],
        "National Politics": ["https://www.sakshi.com/news/national", "https://www.eenadu.net/national"]
    },
    "Sports": {
        "Cricket": ["https://www.sakshi.com/news/sports/cricket", "https://www.eenadu.net/sports/cricket"],
        "Other Sports": ["https://www.sakshi.com/news/sports", "https://www.eenadu.net/sports"]
    },
    "Movies": {
        "Tollywood": ["https://www.sakshi.com/news/movies/tollywood", "https://www.eenadu.net/cinema"],
        "Bollywood": ["https://www.sakshi.com/news/movies/bollywood"],
        "Gossip & Reviews": ["https://www.sakshi.com/news/movies/gossip"]
    },
    "Business": {
        "Markets & Economy": ["https://www.sakshi.com/news/business", "https://www.eenadu.net/business"]
    },
    "Technology": {
        "Tech & Innovation": ["https://www.sakshi.com/news/science-and-technology", "https://www.eenadu.net/technology"]
    },
    "Education": {
        "General Education": ["https://www.sakshi.com/news/education", "https://www.eenadu.net/education"]
    },
    "Health": {
        "Health": ["https://www.sakshi.com/news/health"]
    },
    "Lifestyle": {
        "Family & Lifestyle": ["https://www.sakshi.com/news/family"]
    }
}


def scrape_and_collect(topic, subtopic):
    articles = []
    urls = topic_sites[topic][subtopic]

    for url in urls:
        try:
            print(f"Scraping {url} ...")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup.find_all(["a", "p"]):
                text = tag.get_text(strip=True)
                if text and len(text) > 30:
                    try:
                        if detect(text) == "te":
                            articles.append({
                                "topic": topic,
                                "subtopic": subtopic,
                                "text": text,
                                "url": url
                            })
                    except:
                        pass
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return pd.DataFrame(articles)
