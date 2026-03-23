# Where GitHub Actions runners run

This repository exists for **academic purposes**: to explore and document **where GitHub Actions workflow runners are deployed**, using runner environment details and network-derived location signals from workflow runs.

## Analysis results (`scripts/analyze-report-runs.py`)

Sample output from 100 report runs with readable `ipinfo.json`:

Runs with readable ipinfo.json: 100 (of 100 files)

### Azure region (programmatic name)

| Count | Region |
|------:|--------|
| 20 | northcentralus |
| 17 | eastus2 |
| 12 | westcentralus |
| 12 | westus3 |
| 12 | westus |
| 12 | centralus |
| 11 | eastus |
| 3 | (unmapped) |
| 1 | westus2 |

### Country (ipinfo)

| Count | Country |
|------:|---------|
| 97 | US |
| 3 | (missing) |

### Region (ipinfo)

| Count | Region |
|------:|--------|
| 28 | Virginia |
| 20 | Illinois |
| 12 | Wyoming |
| 12 | Arizona |
| 12 | California |
| 12 | Iowa |
| 3 | (missing) |
| 1 | Washington |

### City (ipinfo)

| Count | City |
|------:|------|
| 20 | Chicago |
| 17 | Boydton |
| 12 | Cheyenne |
| 12 | Phoenix |
| 12 | San Jose |
| 12 | Des Moines |
| 11 | Washington |
| 3 | (missing) |
| 1 | Moses Lake |
