from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configure logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Define your tasks
def scrape_task():
    url = 'https://example.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    for item in soup.find_all('div', class_='example-class'):
        data.append(item.text)
    
    df = pd.DataFrame(data, columns=['column_name'])
    df['cleaned_column'] = df['column_name'].apply(lambda x: x.strip())
    print(df)
    
    
def task_one():
    print("Task one is running")

def another_task():
    print("Another task is running...")

def task_two():
    print("-------------------------------------------------------------------------------------------------------------------------------")

# Create the scheduler
scheduler = BlockingScheduler()

# Add jobs to the scheduler
scheduler.add_job(task_one, IntervalTrigger(minutes=1), id='task_one', replace_existing=True)
scheduler.add_job(another_task, IntervalTrigger(minutes=1), id='another_task', replace_existing=True)
scheduler.add_job(task_two, IntervalTrigger(minutes=1), id='task_two', replace_existing=True)


# Start the scheduler
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
