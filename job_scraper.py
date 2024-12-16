import requests
from bs4 import BeautifulSoup
from plyer import notification
import sqlite3
import time
import yaml
import concurrent.futures
import logging
from job_parsers import parse_h2_structure, parse_tr_structure

DB_PATH = 'job_scraper.db'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                category_location TEXT,
                skills TEXT,
                is_new BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def save_job(job_details):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (title, url, category_location, skills, is_new)
            VALUES (?, ?, ?, ?, ?)
        ''', (job_details['title'], job_details['url'], job_details['category_location'], job_details['skills'], job_details['is_new']))
        conn.commit()

def job_exists(title, url):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM jobs WHERE title=? AND url=?', (title, url))
        return cursor.fetchone() is not None

def get_job_listings(url, job_title):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Combine results from both parsing functions
        jobs = parse_h2_structure(soup, url, job_title)
        jobs.extend(parse_tr_structure(soup, url, job_title))
        
        return jobs
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return []

def send_notification(title, message, url):
    notification.notify(
        title=title,
        message=f"{message}\n{url}",
        app_name='Job Scraper',
        timeout=10
    )

def fetch_jobs_from_site(site, job_title):
    return get_job_listings(site, job_title)

def main():
    init_db()
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    job_title = config['job_title']
    websites = config['websites']
    
    logging.info(f"Starting job scraping for {len(websites)} websites.")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_site = {executor.submit(fetch_jobs_from_site, site, job_title): site for site in websites}
        for future in concurrent.futures.as_completed(future_to_site):
            site = future_to_site[future]
            try:
                jobs = future.result()
                for job in jobs:
                    if not job_exists(job['title'], job['url']):
                        save_job(job)
                        send_notification('New Job Found!', job['title'], job['url'])
                        time.sleep(1)
            except Exception as e:
                logging.error(f"Error processing {site}: {e}")

if __name__ == "__main__":
    main()