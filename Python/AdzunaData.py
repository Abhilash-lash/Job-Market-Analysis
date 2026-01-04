import os
from dotenv import load_dotenv
import requests
import json
import time

all_jobs = []
load_dotenv('Adzuna Keys.env')

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
print(APP_ID, '\n', APP_KEY)

# Limiting to the first 10 pages(500 records) to respect API rate limits
# and demonstrate scalable pagination logic

for i in range(1, 11):
    base_url = f"https://api.adzuna.com/v1/api/jobs/in/search/{i}?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50&where=india&max_days_old=30&sort_by=date"

    response = requests.get(base_url)
    if response.status_code == 200:
        print("Data Retrieved, Page ", i)
        raw_data = response.json()
    else:
        print("Job List Done/Not Found")

    jobs = raw_data['results']
    if not jobs:
        break
    for job in jobs:

        record = {
            'Job_ID': job.get('id'),
            'Job_Title': job.get('title'),
            'Category': job.get('category', {}).get('label'),
            'Date_of_Creation': job.get('created'),
            'Company_Name': job.get('company', {}).get('display_name'),
            'Job_Location': job.get('location', {}).get('display_name')
        }
        all_jobs.append(record)
    time.sleep(1)
print("Total Jobs Availabe on Site:", raw_data.get("count"))
print(len(all_jobs))
