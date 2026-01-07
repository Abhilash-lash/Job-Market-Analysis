import os
from dotenv import load_dotenv
import requests
import json
import time
import csv

all_jobs = []

# API ID and Key are kept in a separate 'env' file for Security
# Extracting the ID and Key using dotenv library
load_dotenv('Adzuna Keys.env')
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
print("\n\nAPI ID and Key extraction Successfull\n\n")


# Limiting to the first 10 pages(500 records) to respect API rate limits
# and demonstrate scalable pagination logic

for i in range(1, 11):
    base_url = f"https://api.adzuna.com/v1/api/jobs/in/search/{i}?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50&what=data%20analyst&where=india&max_days_old=60&sort_by=date"

    response = requests.get(base_url)
    if response.status_code == 200:
        print("Data Retrieved, Page ", i)
        raw_data = response.json()
    else:
        print("Job List Done/Not Found")
        continue

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
            'Job_Location': job.get('location', {}).get('display_name'),
            'Description': job.get('description')
        }
        all_jobs.append(record)
    time.sleep(1)
print("Total Jobs Availabe on Site:", raw_data.get("count"))
print(len(all_jobs))

# Block to write the extracted Data to a CSV file

csv_filename = "Adzuna_Data_Jobs.csv"
field_names = ['Job_ID', 'Job_Title', 'Category',
               'Date_of_Creation', 'Company_Name', 'Job_Location', 'Description']

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(all_jobs)
    print('\n\n Data Dump to CSV File --ALL DONE')
