
from __future__ import print_function
import os
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


KEEP_PATH = r'D:\Desktop\Keep'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']

def parse_json():
    tasks = []
    for entry in os.scandir(KEEP_PATH):
        if (entry.path.endswith(".json") and entry.is_file()):
            task = {}
            with open(entry.path, encoding="utf-8") as json_file:
                print(entry.path)
                data = json.load(json_file)
                if 'title' in data:
                    task['title'] = data['title']
                else:
                    task['title'] = ''
                if 'textContent' in data:
                    task['notes'] = data['textContent']
                else:
                    task['notes'] = ''
                if 'listContent' in data:
                    for li in data['listContent']:
                        task['notes'] += li['text'] + '\n'

            tasks.append(task)
    return tasks

def connect_service():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)
    return service

def delete_all_tasks():
    service = connect_service()
    tasks = service.tasks().list(tasklist='@default').execute()
    for task in tasks['items']:
        print('deleting ' + task['id'])
        service.tasks().delete(tasklist='@default', task=task['id']).execute()

def upload_tasks():
    service = connect_service()
    tasks = parse_json()
    for task in tasks:
        result = service.tasks().insert(tasklist='@default', body=task).execute()
        print(result['id'])


def main():
    upload_tasks()

main()
