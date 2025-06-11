import asyncio
import aiohttp
import csv
import re
from pathlib import Path
from datetime import date
from typing import List, Dict, Optional

CSV_FILE = Path(f"../data/new/{date.today()}-new_sponsors.csv")

"""
1. Search Google for a company website (e.g., "Agroexcel International Ltd") using googlesearch-python.
2. Filter results to find the company’s real website — match name in domain/title, exclude certain domains like find-and-update.company-information.service.gov.uk.
3. Visit pages on the site (like About, Contact, or Formation pages) to locate the correct page.
4. Extract email addresses from those pages.
5. Do this task async for all companies
6. Schedule this task everyday
"""


