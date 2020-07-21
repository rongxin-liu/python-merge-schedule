# python-merge-schedule-action

> A python-based GitHub action to merge pull requests at a scheduled time

> Inspired by https://github.com/marketplace/actions/merge-schedule

## Usage

Create `.github/workflows/main.yml`

```yml
name: Python Merge Schedule
on:
  pull_request:
    types:
      - opened
      - edited
  schedule:
    - cron: "1/15 * * * *"

jobs:
  merge_schedule:
    runs-on: ubuntu-latest
    steps:
      - uses: rongxin-liu/python-merge-schedule@v1.x
        env:
          TIMEZONE: America/New_York
```

Specify a timezone using the [TZ database name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

In the pull request, add a line using the following syntax to set a PR merge schedule:

```
/schedule Sun 6/21 11:59pm
```
