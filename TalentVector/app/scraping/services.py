from app.jobs.models import JobOffer

from .scrappers.infojobs_scraper import InfoJobsScraper

def save_jobs(jobs):
    saved = 0
    skipped = 0
    for job in jobs:
        if not job['url']:
            skipped +=1
            continue
        if JobOffer.objects(url=job['url']).first():
            skipped += 1
            continue

        JobOffer(**job).save()
        saved += 1

    return saved, skipped


def run_scraping():
    scraper = InfoJobsScraper()
    jobs = scraper.scrape()
    saved, skipped = save_jobs(jobs)
    return {
        'total_scrapped': len(jobs),
        'saved': saved,
        'skipped': skipped
    }