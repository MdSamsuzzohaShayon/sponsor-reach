# Compares today's vs previous CSV to detect changes
# extraction/compare_csv.py

import os
import shutil
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from config.constants import REQUIRED_COLS, ORGANIZATION_NAME, ARCHIVE_DIR
from extraction.parse_sponsors import preprocess_sponsor_data


raw_dir = './data/raw'


def find_file_with_date(dir_path: str, date_str: str) -> Optional[str]:
    """
    Look for a CSV file in a directory containing a specific date string in its filename.
    Returns the file path if found, otherwise None.
    """
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
    for file in files:
        if date_str in os.path.basename(file):
            return file
    return None

def clean_old_files(dir_path: str, keep_dates: set):
    """
    Delete CSV files in a directory that don't contain any of the specified dates.
    """
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
    for file in files:
        if not any(date in os.path.basename(file) for date in keep_dates):
            os.remove(file)
            print(f"Deleted old file: {file}")



def get_yesterday_file(directory: str) -> str:
    """
    Implements:
    1. Check if yesterday's file exists in archive.
    2. If not, check raw directory — move it to archive if found.
    3. Then check archive for files from the 4 days before yesterday.
    4. Delete all archive files older than last 5 days.
    """
    raw_dir = './data/raw'

    # Build date strings for yesterday and the last 5 days (including yesterday)
    date_strs = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 6)]
    yesterday_str = date_strs[0]

    # ✅ Logic 1: Check yesterday's file in archive
    file_in_archive = find_file_with_date(ARCHIVE_DIR, yesterday_str)
    if file_in_archive:
        clean_old_files(ARCHIVE_DIR, set(date_strs))
        return file_in_archive

    # ✅ Logic 2: Check yesterday's file in raw and move it to archive
    file_in_raw = find_file_with_date(raw_dir, yesterday_str)
    if file_in_raw:
        if not os.path.exists(ARCHIVE_DIR):
            os.makedirs(ARCHIVE_DIR)
        file_name = os.path.basename(file_in_raw)
        archive_path = os.path.join(ARCHIVE_DIR, file_name)
        shutil.move(file_in_raw, archive_path)
        print(f"Moved yesterday's file from raw to archive: {archive_path}")
        clean_old_files(ARCHIVE_DIR, set(date_strs))
        return archive_path

    # ✅ Logic 3: Check last 4 days before yesterday in archive
    for date_str in date_strs[1:]:  # Skipping yesterday_str (already checked)
        file_in_archive = find_file_with_date(ARCHIVE_DIR, date_str)
        if file_in_archive:
            clean_old_files(ARCHIVE_DIR, set(date_strs))
            return file_in_archive

    # ✅ Clean up old files anyway
    clean_old_files(ARCHIVE_DIR, set(date_strs))
    raise FileNotFoundError("No CSV file from the last 5 days found in either archive or raw directories.")


def get_new_sponsors(df_latest: pd.DataFrame, df_previous: pd.DataFrame) -> list[dict]:
    """
    Compare today's CSV with yesterday's and return list of new sponsor rows (as dicts),
    based on unique combination of Organisation Name and Route.
    """


    # Ensure the necessary columns exist
    if not REQUIRED_COLS.issubset(df_latest.columns) or not REQUIRED_COLS.issubset(df_previous.columns):
        raise ValueError(f"Missing required columns. Needed: {REQUIRED_COLS}")

    # Create sets of (Organisation Name, Route) tuples
    latest_set = set(zip(df_latest[ORGANIZATION_NAME].astype(str), df_latest['Route'].astype(str)))
    previous_set = set(zip(df_previous[ORGANIZATION_NAME].astype(str), df_previous['Route'].astype(str)))

    # Find new entries
    new_entries = latest_set - previous_set

    # Filter the latest DataFrame to get new sponsor rows
    new_sponsors_df = df_latest[df_latest.apply(
        lambda row: (str(row[ORGANIZATION_NAME]), str(row['Route'])) in new_entries, axis=1
    )]

    return new_sponsors_df.to_dict(orient='records')



