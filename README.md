**Job Search Automation Tool**
=============================

Searching for a job is tedious. Going through websites each and every day to search for jobs is annoying and frustrating. This tool automates the process of job searching by scraping job listings from specified websites and sending desktop notifications for jobs that match a specific title.

## Project Structure
```java
job_scraper/
├── job_scraper.py
├── job_parsers.py
├── requirements.txt
├── config.yaml
```

**Usage**
-----

### Windows

1. Install the required libraries by running `pip install -r requirements.txt`
2. Run the script by executing `python job_scraper.py`
3. Follow the prompts to set up the script

### Linux/Mac

1. Install the required libraries by running `pip3 install -r requirements.txt`
2. Run the script by executing `python3 job_scraper.py`
3. Follow the prompts to set up the script

**Setup**
-----

1. Edit the `config.yaml` file to specify the websites and job titles you want to search for. Here is an example of how the `config.yaml` file should look:
   ```yaml
   job_title: "Engineer"
   websites:
     - https://careers.upstart.com/jobs/search
     # Add more websites here
   ```

2. Set up a scheduler to run the script at regular intervals (e.g. daily)

**Scheduler Setup**
-----------------

### Windows

1. Open the Task Scheduler: You can search for it in the Start menu or type `taskschd.msc` in the Run dialog box (Windows key + R)
2. Create a new task: Right-click on "Task Scheduler" in the left panel and select "Create Basic Task"
3. Set the trigger: Click on the "Triggers" tab and then click "New". Select "Daily" and set the start time to your preferred time
4. Set the action: Click on the "Actions" tab and then click "New". Select "Start a program" and enter the path to your Python executable (e.g. `C:\Python39\bin\python.exe`). Add the script file as an argument (e.g. `C:\Path\To\Your\Script\main.py`)

### Linux/Mac

1. Open your terminal and run `crontab -e` to edit your cron table
2. Add the following line to run the script daily at 8am: `0 8 * * * python /path/to/your/script/main.py`

**How to Use the Tool**
----------------------

1. **Define Your Job Title Search Keywords:**
   - In the `config.yaml` file, specify the job titles you're interested in. For example:
     ```yaml
     job_title: "Engineer"
     ```

2. **Add Websites to Scrape:**
   - In the `config.yaml` file, specify the websites you want to scrape. For example:
     ```yaml
     websites:
       - "https://boards.greenhouse.io/himshers"
       - "https://www.celigo.com/careers/#job-listings"
       - "https://careers.upstart.com/jobs/search"
     ```

3. **Run the Script:**
   - Follow the instructions under the **Usage** section to run the script and follow the prompts to set it up.

# Troubleshooting
1. **No Notifications:**
  * Ensure that your system supports desktop notifications and that the plyer library is correctly installed and configured.
2. **Network Errors:**
  * Check your internet connection and ensure the URLs in config.yaml are accessible.
3. **HTML Structure Changes:** 
  * If the script fails to find job listings, the HTML structure of the target websites may have changed. Update the parsing logic in job_parsers.py to match the new structure.
4. **Missing Dependencies:**
  * Ensure all dependencies are installed by running pip install -r requirements.txt.
5. **Script Crashes:**
  * Check the logs for error messages and stack traces to identify the issue. Ensure that the config.yaml file is correctly formatted.

**Growth and Contribution**
-------------------------

* Add more websites to scrape job listings from
* Improve the script to handle different types of job listings (e.g. freelance, internship)
* Add more features to the script (e.g. email notifications, job application tracking)
* Contribute to the script by fixing bugs and improving performance
git a

**Credit**
---------
* This tool credits [Joanne Mok](https://www.linkedin.com/posts/joanne-mok-832b78175_additional-56-companies-that-are-hiring-for-activity-7219680376397385728-h2YI?utm_source=share&utm_medium=member_desktop) for curating the list of jobs that I have included in `jobs.md`
