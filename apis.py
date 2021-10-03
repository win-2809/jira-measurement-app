import requests
import json

def getJiraIssue(username, token, domain, projectKey, startAt):
    headers = {
            'Content-Type': 'application/json'
        }
    
    params = {
        "jql": "project = " + projectKey,
        "fieldsByKeys": "false",
        "fields": ["summary","status","assignee","created","issuetype","priority","creator","versions","labels","updated","components"],
        "startAt": startAt,
        "maxResults": 100
    }

    response = requests.get(f"{domain}/rest/api/3/search", auth=(username, token), headers=headers, params=params).json()

    return response