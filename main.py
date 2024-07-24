import requests
from bs4 import BeautifulSoup
from plyer import notification
import sqlite3
import time
from urllib.parse import urljoin
import yaml

DB_PATH = 'job_scraper.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_job(title, url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO jobs (title, url) VALUES (?, ?)', (title, url))
    conn.commit()
    conn.close()

def job_exists(title, url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE title=? AND url=?', (title, url))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_job_listings(url, job_title):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_listings = soup.find_all('div', class_='opening')
    filtered_jobs = [job for job in job_listings if job_title.lower() in job.text.lower()]
    return filtered_jobs

def send_notification(title, message, url):
    notification.notify(
        title=title,
        message=f"{message}\n{url}",
        app_name='Job Scraper',
        timeout=10
    )

if __name__ == "__main__":
    init_db()
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    job_title = config['job_title']
    websites = config['websites']
    
    for site in websites:
        jobs = get_job_listings(site, job_title)
        for job in jobs:
            job_title = job.find('a').text
            job_url = urljoin(site, job.find('a')['href'])  # Use urljoin to handle the URL correctly
            if not job_exists(job_title, job_url):
                save_job(job_title, job_url)
                send_notification('New Job Found!', job_title, job_url)
                time.sleep(1)  # To avoid rate-limiting issues
