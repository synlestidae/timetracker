import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys

from win10toast import ToastNotifier

from datetime import datetime

parser = argparse.ArgumentParser(description='Begin logging time for a task')

parser.add_argument('task', type=str, help='ID of the task you are working on')
parser.add_argument('comment', type=str, help='What you are doing')
parser.add_argument('username', type=str, help='Your Atlassian username')
parser.add_argument('password', type=str, help='Your Atlassian password')

args = parser.parse_args()

session = requests.Session()
session.auth = (args.username, args.password)

print("Beginning logging for task %s: %s" % (args.task, args.comment))

started_at = datetime.utcnow()
seconds = 0
time_taken = None

has_err = False

toaster = ToastNotifier()
#toaster.show_toast("Let's go!","We've started tracking work on %s" % args.task)

while 1:
    command = str(input("Enter a command (done, status, recover): ")).strip()

    if command == 'recover':
        has_err = False

    if not has_err: 
        time_taken = datetime.utcnow() - started_at
        print("You have been working on %s for about %d minutes (or exactly %d seconds)." % (args.task, time_taken.seconds / 60, time_taken.total_seconds()))
    else:
        print("In error state. Use recover command to update the started_at time to now")

    if command == 'done':
        seconds = time_taken.total_seconds()
        if input("Log to Jira? (Y/N) ").lower().strip() == 'y':
           url = "rest/api/2/issue/%s/worklog" % args.task
           request_body = {
                'comment':  args.comment,
                'started': started_at.isoformat()[:-3] + '+1300', #
                'timeSpent': "%dm" % ((seconds / 60) + 1)
           }
           try: 
               full_url = "https://raygun.atlassian.net/%s" % url
               print("Posting log to " + full_url)
               print(request_body)
               result = requests.post(full_url, json=request_body, auth=HTTPBasicAuth(args.username, args.password))
               if result.status_code >= 400:
                   print("Jira API gave status code %d" % result.status_code)
                   print(result.content)
                   has_err = True
               else:
                   print("Cool! Time logged")
                   sys.exit(0)
           except Exception as e: 
               print("There was an exception while posting")
               print(e)
               has_err = True
               continue  

