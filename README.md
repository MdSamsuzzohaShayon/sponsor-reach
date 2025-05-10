## UK Sponsor Reach

This project automates the process of monitoring, enriching, and syncing the UK Government's Worker and Temporary Worker Sponsor Licence register with a Salesforce CRM. It performs data extraction, enrichment, email outreach, and ensures that sponsor records are kept up-to-date.

---

### Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

---

## Overview

The pipeline performs the following steps:
1. **Download the latest CSV** from the UK Government's Sponsor Licence Register.
2. **Compare** the new CSV to the previous one to detect newly added sponsors.
3. **Enrich** sponsor data (e.g., owner, HR contact, industry type, etc.) using third-party APIs.
4. **Send personalized outreach emails** to relevant contacts (owners, HR directors, etc.).
5. **Sync** the enriched data to Salesforce CRM, adding new records, updating existing records, and archiving those that are no longer listed.

---

## Prerequisites

1. Python 3.8 or higher
2. Git
3. A Salesforce account with API access (Optional for now)
4. Valid SMTP credentials for email sending (Optional for now)
5. AWS credentials (optional, for cloud deployment) 

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/mdsamsuzzohashayon/sponsor-reach.git
cd sponsor-reach
```

### 2. Set up a virtual environment
We recommend using a virtual environment to manage dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate  
# On Windows, use `.venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

### 1. Create a `.env` file
Copy the `.env.example` file to create your own `.env` file and update the values with your credentials:


---

## Usage

### 1. Running the Pipeline

To start the pipeline and execute all stages (download, comparison, enrichment, outreach, CRM sync), run:

```bash
python main.py
```


---

## File Structure

```
uk_sponsor_pipeline/
│
├── config/
│   └── settings.py              # Configuration for API keys, file paths, etc.
│
├── data/
│   ├── raw/                     # Downloaded CSVs from UK Gov (daily snapshots)
│   ├── enriched/                # Cleaned & enriched sponsor data
│   ├── logs/                    # Daily run logs, error logs
│   └── archive/                 # Archived CSVs after processing
│
├── extraction/
│   ├── download_csv.py          # Downloads latest UK Gov CSV
│   ├── compare_csv.py           # Compares today's vs previous CSV to detect changes
│   └── parse_sponsors.py        # Preprocesses CSV using pandas
│
├── enrichment/
│   ├── enrich_company.py        # Enriches a company using APIs (Clearbit, SerpAPI, etc.)
│   ├── enrich_batch.py          # Loops through new companies and enriches all
│   └── utils.py                 # Helper for validation, standardizing names, etc.
│
├── outreach/
│   ├── email_templates/         # HTML/Jinja2 templates for email campaigns
│   ├── send_email.py            # Sends personalized emails using SendGrid/Mailgun
│   └── outreach_runner.py       # Picks enriched contacts and launches email
│
├── crm/
│   ├── salesforce_api.py        # Auth, create, update, archive sponsor records
│   └── sync_crm.py              # Handles syncing pipeline from enriched data to Salesforce
│
├── scheduler/
│   ├── daily_workflow.py        # Main runner: extraction → enrichment → email → CRM
│   └── cronjob.sh               # Shell script to run via cron / task scheduler
│
├── utils/
│   ├── logger.py                # Central logging and error handling
│   └── monitor.py               # Sends alerts via email/Slack on failure
│
├── tests/
│   ├── test_compare.py          # Unit tests for CSV difference detection
│   ├── test_enrichment.py       # Tests for mock API enrichment
│   ├── test_email.py            # Tests email formatting and send simulation
│   └── test_salesforce.py       # Tests for CRM integration
│
├── .env                         # Environment variables (API keys, tokens)
├── requirements.txt             # Python dependencies (pandas, requests, etc.)
├── README.md                    # This file
└── main.py                      # Entry point – executes `daily_workflow`
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
