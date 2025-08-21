
import requests
import time
import os
# 🔑 API Keys (Replace with your actual keys)
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
# FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"
# # 🔗 API URLs
# FIRECRAWL_START_URL = FIRECRAWL_BASE_URL
# FIRECRAWL_STATUS_URL = "https://api.firecrawl.ai/status"
# FIRECRAWL_RESULTS_URL = "https://api.firecrawl.ai/results"
#
# # Step 1: Start Firecrawl AI-powered web scraping
# firecrawl_payload = {
#     "domain": "https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide",
#     # "keywords": ["AI", "Machine Learning"],
#     "max_pages": 5
# }
#
# firecrawl_response = requests.post(
#     FIRECRAWL_START_URL,
#     json=firecrawl_payload,
#     headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
# )
# firecrawl_data = firecrawl_response.json()
#
# # Extract Crawl ID
# crawl_id = firecrawl_data.get("crawl_id")
# if not crawl_id:
#     print("❌ Error: Failed to start Firecrawl.")
#     exit()
#
# print(f"🚀 Firecrawl started! Crawl ID: {crawl_id}")
#
# # Step 2: Monitor Crawl Status
# while True:
#     status_response = requests.get(
#         f"{FIRECRAWL_STATUS_URL}/{crawl_id}",
#         headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
#     )
#     status_data = status_response.json()
#     status = status_data.get("status")
#
#     print(f"⏳ Status: {status}")
#
#     if status == "completed":
#         break
#     elif status in ["failed", "error"]:
#         print("❌ Firecrawl failed.")
#         exit()
#
#     time.sleep(5)
#
# # Step 3: Fetch Crawl Results
# results_response = requests.get(
#     f"{FIRECRAWL_RESULTS_URL}/{crawl_id}",
#     headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}"}
# )
# results_data = results_response.json()
# articles = results_data.get("articles", [])
# print(articles)
#


'''
curl -X POST https://api.firecrawl.dev/v1/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer fc-54f5d81344d34207ae1ba87ac565458d' \
    -d '{
        "url": "https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide",
		"formats": [ "markdown" ],
		"onlyMainContent": true,
		"parsePDF": true,
		"maxAge": 14400000
	}'
'''

# Install with pip install firecrawl-py
import asyncio
from firecrawl import AsyncFirecrawlApp, FirecrawlApp

url = 'https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide'
url = "https://news.hada.io/topic?id=22490"
url = "https://old.reddit.com/r/LocalLLaMA/comments/1mke7ef/120b_runs_awesome_on_just_8gb_vram/"

def main():
    app = FirecrawlApp(api_key='fc-54f5d81344d34207ae1ba87ac565458d')
    response = app.scrape_url(
        url=url,
        formats= [ 'markdown' ],
        only_main_content= True,
        parse_pdf= True,
        max_age= 14400000
    )
    with open('temp/firecrawl_response.md', 'w') as f:
        f.write(response.markdown)

if __name__ == '__main__':
    main()
