from urllib.parse import urljoin
from bs4 import BeautifulSoup

def parse_h2_structure(soup, url, job_title):
    jobs = []
    job_listings = soup.find_all('h2')
    for job in job_listings:
        job_anchor = job.find('a')
        if job_anchor and job_title.lower() in job_anchor.text.lower():
            job_title_text = job_anchor.text.strip()
            job_url = urljoin(url, job_anchor['href'])
            
            info_bar = job.find_next_sibling('div', class_='info-bar')
            if info_bar:
                category_location = info_bar.find('div', class_='category-location').text.strip()
                skills = info_bar.find('span', class_='skills').text.strip()
                is_new = info_bar.find('span', class_='new') is not None
            
            jobs.append({
                'title': job_title_text,
                'url': job_url,
                'category_location': category_location,
                'skills': skills,
                'is_new': is_new
            })
    return jobs

def parse_tr_structure(soup, url, job_title):
    jobs = []
    job_listings = soup.find_all('tr', {'data-action': 'click->jobs--table-results#navigate'})
    for job in job_listings:
        job_anchor = job.find('td', class_='job-search-results-title').find('a')
        if job_anchor and job_title.lower() in job_anchor.text.lower():
            job_title_text = job_anchor.text.strip()
            job_url = urljoin(url, job_anchor['href'])
            
            category = job.find('td', class_='job-search-results-category').find('li').text.strip()
            location = job.find('td', class_='job-search-results-location').find('li')
            location_text = location.text.strip() if location else "Not specified"
            workplace_type = job.find('td', class_='job-search-results-workplace-types').text.strip()
            
            jobs.append({
                'title': job_title_text,
                'url': job_url,
                'category_location': f"{category} in {location_text}",
                'skills': "Not specified",  # Assuming skills are not provided in this structure
                'is_new': False  # Assuming no 'new' indicator in this structure
            })
    return jobs