import logging
import os
import re
import traceback
from github import Github
from datetime import datetime
from dateutil import parser
from pytz import reference, timezone

logging.basicConfig(level=logging.INFO)

TIMEZONE = os.getenv("TIMEZONE")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

def get_schedule(pull):
    """Extract the scheduled time from PR's description"""
    try:
        scheduled_time = pull.body.splitlines()[-1].split("/schedule")[1].strip()
        return int(parser.parse(scheduled_time).timestamp() - tz_offset())
    except:
        pass


def get_scheduled_pulls(repo):
    """Get all PRs that are scheduled to merge"""
    scheduled_pulls = []
    pulls = repo.get_pulls(state='open', sort='created', base='master')
    for pull in pulls:
        try:
            if get_schedule(pull) > int(datetime.now().timestamp()):
                scheduled_pulls.append(pull)
        except:
            pass

    logging.info(f"Found {len(scheduled_pulls)} PR(s) scheduled to merge")
    return scheduled_pulls


def get_due_pulls(repo):
    """Get all PRs that are due for merging"""
    due_scheduled_pulls = []
    pulls = repo.get_pulls(state='open', sort='created', base='master')
    for pull in pulls:
        try:
            if get_schedule(pull) <= int(datetime.now().timestamp()):
                due_scheduled_pulls.append(pull)
        except:
            pass

    logging.info(f"Found {len(due_scheduled_pulls)} PR(s) due for merging")
    return due_scheduled_pulls


def merge(pull):
    """Merge PR when it is due"""
    try:
        logging.info(f"Attempt to merge PR #{pull.number}: {pull.title[:20]} <-> {pull.base.label}")
        SHA = pull.merge().sha
        logging.info(f"Merged! Commit URL: https://github.com/{GITHUB_REPOSITORY}/commit/{SHA}")
    except:
        logging.info(f"Failed to merge PR #{pull.number}")
        traceback.print_exc()


def tz_offset():
    """Calculate timezone offset between user timezone and UTC timezone"""
    tz_user = parser.parse(str(datetime.now(timezone(TIMEZONE)))[:-6]).timestamp()
    tz_github = parser.parse(str(datetime.now(timezone("UTC")))[:-6]).timestamp()
    return int(tz_user - tz_github)


if __name__ == "__main__":
    logging.info(f"Action triggered at: {datetime.now()}")
    client = Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPOSITORY)    
    try:
        get_scheduled_pulls(repo)
        for due_pull in get_due_pulls(repo):
            merge(due_pull)
    except:
        traceback.print_exc()
    