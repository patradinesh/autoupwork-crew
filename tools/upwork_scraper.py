from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime

def search_upwork_jobs():
    results = []
    keywords = ["DevOps", "Cloud Engineering", "Kubernetes", "AWS", "CI/CD"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to False for debugging
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        page = context.new_page()

        query = "+".join(keywords)
        url = f"https://www.upwork.com/ab/jobs/search/?q={query}&sort=recency"

        try:
            print(f"[INFO] Navigating to {url}")
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle", timeout=30000)

            print("[INFO] Waiting for job cards to load...")
            page.wait_for_selector("section.air-card", timeout=30000)

            job_cards = page.query_selector_all("section.air-card")
            if not job_cards:
                print("[WARN] No job cards found.")
                return results

            for job in job_cards[:5]:
                title_el = job.query_selector("a.job-title-link")
                if not title_el:
                    continue

                title = title_el.inner_text().strip()
                link = "https://www.upwork.com" + title_el.get_attribute("href")

                posted_el = job.query_selector("span[data-test='posted-on']")
                posted_time = posted_el.inner_text().strip() if posted_el else "N/A"

                budget_el = job.query_selector("strong[data-test='budget']")
                budget = budget_el.inner_text().strip() if budget_el else "N/A"

                results.append({
                    "title": title,
                    "link": link,
                    "posted": posted_time,
                    "budget": budget
                })

        except PlaywrightTimeoutError as e:
            print(f"[ERROR] Timed out waiting for selector: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
        finally:
            browser.close()

    return results
