# python-merge-schedule-action

> A python-based GitHub action to merge pull requests at a scheduled time

> Inspired by https://github.com/marketplace/actions/merge-schedule

## Usage

1. Create a GitHub workflow config file in the target repo: `.github/workflows/main.yml`

If this GitHub action is defined in a private repository (current scenario):

```yml
name: Python Merge Schedule
on:
  pull_request:
    types:
      - opened
      - edited
  schedule:
    - cron: '*/15 * * * *'

jobs:
  python-merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          repository: organization/python-merge-schedule
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          path: python-merge-schedule
      - uses: ./python-merge-schedule
        env:
          TIMEZONE: America/New_York
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

If the GitHub action is defined in a public repository:

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
      - uses: organization/python-merge-schedule@v1.x
        env:
          TIMEZONE: America/New_York
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

`TIMEZONE`: Configure the timezone using the [TZ database name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
`PERSONAL_ACCESS_TOKEN `: When the action is defined in the private repository, you will need to configure a GitHub personal access token and use it to check out the GitHub action and use it.

In the pull request, add a line using the following syntax to set a PR merge schedule:

```
/schedule Sun 6/21 11:59pm
```
