# Where GitHub Actions runners run

This repository exists for **academic purposes**: to explore and document **where GitHub Actions workflow runners are deployed**, using runner environment details and network-derived location signals from workflow runs.

## Analysis results (`scripts/analyze-report-runs.py`)

Sample output from 300 report runs with readable `ipinfo.json`:

Runs with readable ipinfo.json: 300 (of 300 files)

### Azure region (programmatic name)

| Count | Region |
|------:|--------|
| 66 | westus |
| 55 | northcentralus |
| 55 | eastus |
| 52 | eastus2 |
| 24 | centralus |
| 23 | westcentralus |
| 23 | westus3 |
| 2 | westus2 |

### Country (ipinfo)

| Count | Country |
|------:|---------|
| 300 | US |

### Region (ipinfo)

| Count | Region |
|------:|--------|
| 107 | Virginia |
| 66 | California |
| 55 | Illinois |
| 24 | Iowa |
| 23 | Wyoming |
| 23 | Arizona |
| 2 | Washington |

### City (ipinfo)

| Count | City |
|------:|------|
| 66 | San Jose |
| 55 | Chicago |
| 55 | Washington |
| 52 | Boydton |
| 24 | Des Moines |
| 23 | Cheyenne |
| 23 | Phoenix |
| 2 | Moses Lake |
