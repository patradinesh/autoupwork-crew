from tools.upwork_scraper import search_upwork_jobs

if __name__ == "__main__":
    jobs = search_upwork_jobs()
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Link: {job['link']}")
        print(f"Posted: {job['posted']}")
        print(f"Budget: {job['budget']}")
        print("-" * 50)
