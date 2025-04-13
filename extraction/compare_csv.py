# Compares today's vs previous CSV to detect changes
# extraction/compare_csv.py

import os
import shutil
import pandas as pd
from datetime import datetime, timedelta


def get_latest_file(directory: str) -> str:
    """Return the most recently modified file in the directory."""
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    if not files:
        raise FileNotFoundError("No CSV files found in the directory.")
    return max(files, key=os.path.getmtime)

# def find_file_in_directory(dir_path):
#     yesterday = datetime.now() - timedelta(days=1)
#
#     files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
#     for file in files:
#         modified_time = datetime.fromtimestamp(os.path.getmtime(file))
#         if modified_time.date() == yesterday.date():
#             return file
#     return None


def find_file_in_directory(dir_path):
    """Returns the first CSV file containing yesterday's date in its filename, or None."""
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
    for file in files:
        if yesterday_str in os.path.basename(file):
            return file
    return None

def get_yesterday_file(directory: str) -> str:
    """
    Tries to find a file modified yesterday in the given directory.
    If not found in 'archive', checks 'raw' directory and moves it to 'archive'.
    Returns the file path.
    """




    # First check in archive directory
    archive_dir = './data/archive'
    raw_dir = './data/raw'

    file_in_archive = find_file_in_directory(archive_dir)
    if file_in_archive:
        return file_in_archive

    # If not found, check in raw directory
    file_in_raw = find_file_in_directory(raw_dir)
    if file_in_raw:
        # Move it to archive
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)

        file_name = os.path.basename(file_in_raw)
        archive_path = os.path.join(archive_dir, file_name)
        shutil.move(file_in_raw, archive_path)
        print(f"Moved yesterday's file from raw to archive: {archive_path}")
        return archive_path

    raise FileNotFoundError("No CSV file from yesterday found in either archive or raw directories.")


def get_new_sponsors(latest_csv_path: str) -> list[dict]:
    """
    Compare today's CSV with yesterday's and return list of new sponsor rows (as dicts),
    based on unique combination of Organisation Name and Route.
    """

    # Load latest and previous CSVs
    df_latest = pd.read_csv(latest_csv_path)
    archive_dir = './data/archive'
    previous_csv_path = get_yesterday_file(archive_dir)
    df_previous = pd.read_csv(previous_csv_path)

    # Ensure the necessary columns exist
    required_cols = {'Organisation Name', 'Route'}
    if not required_cols.issubset(df_latest.columns) or not required_cols.issubset(df_previous.columns):
        raise ValueError(f"Missing required columns. Needed: {required_cols}")

    # Create sets of (Organisation Name, Route) tuples
    latest_set = set(zip(df_latest['Organisation Name'].astype(str), df_latest['Route'].astype(str)))
    previous_set = set(zip(df_previous['Organisation Name'].astype(str), df_previous['Route'].astype(str)))

    # Find new entries
    new_entries = latest_set - previous_set

    # Filter the latest DataFrame to get new sponsor rows
    new_sponsors_df = df_latest[df_latest.apply(
        lambda row: (str(row['Organisation Name']), str(row['Route'])) in new_entries, axis=1
    )]

    return new_sponsors_df.to_dict(orient='records')
