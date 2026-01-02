#!/usr/bin/env python3
import requests
import sys
import argparse

def get_push_commit_count(repo_name, before, head):
    """Return the number of commits in a push using the compare API."""
    url = f"https://api.github.com/repos/{repo_name}/compare/{before}...{head}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("total_commits", 0)
    else:
        return 0
    

def get_events(username):

    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)

    if response.status_code == 200:
        events = response.json() 
        print(f"Events for {username}:")
        for event in events:
            if event['type'] == "PushEvent":
                repo_name = event['repo']['name']
                before = event['payload']['before']
                head = event['payload']['head']

                commit_count = get_push_commit_count(repo_name, before, head)

                print(f"Pushed {commit_count} commit(s) to {repo_name}")
            elif event['type'] == "PullRequestEvent":
                pr_action = event['payload']['action']
                pr_name = event['payload']['pull_request']['title']
                repo_name = event['repo']['name']
                
                print(f"{pr_action} pull request {pr_name} in {repo_name}")
            elif event['type'] == "IssuesEvent":
                print(f"Opened a new issue in {event['repo']['name']}")

            elif event["type"] == "CreateEvent":
                ref_type = event["payload"].get("ref_type", "unknown")
                ref_name = event["payload"].get("ref", event["repo"]["name"])
                print(f"{event['actor']['login']} created {ref_type} '{ref_name}' in {event['repo']['name']}")
            
            elif event['type'] == 'ForkEvent':
                print(f"{event['actor']['login']} forked {event['repo']['name']} → {event['payload']['forkee']['full_name']}")
            
            elif event['type'] == 'WatchEvent':
                if event['payload']['action'] == 'started':
                    print(f"Starred {event['repo']['name']}")
            elif event['type'] == 'DeleteEvent':
                ref_type = event['payload']['ref_type']
                ref_name = event['payload']['ref']
                repo_name = event['repo']['name']

                print(f'{username} deleted {ref_type} {ref_name} in {repo_name}')
    else:
        print("Error:", response.status_code, response.text)


def main():

    parser = argparse.ArgumentParser(description="GitHub activity CLI")
    parser.add_argument("username")
    args = parser.parse_args()

    get_events(args.username)