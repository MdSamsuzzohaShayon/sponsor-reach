# extraction/parse_sponsors.py

import pandas as pd
import logging
from typing import List, Dict
from config.constants import FILE_COLS, REQUIRED_COLS, ORGANIZATION_NAME

# Set up logger
logger = logging.getLogger("parse_sponsors")

def preprocess_sponsor_data(csv_path: str) -> pd.DataFrame:
    """
    Preprocess the sponsor data CSV.
    This function will clean the data, fill missing values, and ensure it's ready for comparison and enrichment.

    Parameters:
    - csv_path: The file path to the CSV file to process.

    Returns:
    - A cleaned pandas DataFrame ready for further processing.
    """

    try:
        # Read CSV file
        logger.info(f"⬇️ Reading CSV data from {csv_path}")
        df = pd.read_csv(csv_path)

        # Check if expected columns are present
        missing_cols = FILE_COLS - set(df.columns)
        if missing_cols:
            logger.error(f"❌ Missing columns in CSV: {', '.join(missing_cols)}")
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        # Remove any rows with missing 'Organisation Name' or 'Route'
        logger.info("🧹 Cleaning data by removing rows with missing 'Organisation Name' or 'Route'")
        subset = list(REQUIRED_COLS) # Convert set to list
        df_cleaned = df.dropna(subset=subset)

        # Additional checks and cleaning
        logger.info("🔄 Ensuring that 'Route' column is in string format")
        df_cleaned['Route'] = df_cleaned['Route'].astype(str)

        # Standardizing 'Organisation Name' to title case to ensure consistency
        logger.info("🔄 Standardizing 'Organisation Name' to title case")
        df_cleaned[ORGANIZATION_NAME] = df_cleaned[ORGANIZATION_NAME].str.title()

        # Additional cleanup for 'Town/City' and 'County' columns if necessary
        logger.info("🔄 Cleaning 'Town/City' and 'County' columns by filling NaN values with 'Unknown'")
        df_cleaned['Town/City'] = df_cleaned['Town/City'].fillna('Unknown')
        df_cleaned['County'] = df_cleaned['County'].fillna('Unknown')

        # If there are any rows with missing or erroneous values in 'Route', handle them
        logger.info("🔄 Handling missing or invalid 'Route' values")
        df_cleaned['Route'] = df_cleaned['Route'].replace('nan', 'Unknown')

        logger.info(f"✅ Data preprocessing complete. Processed {len(df_cleaned)} sponsor entries.")
        return df_cleaned

    except FileNotFoundError as fnf_error:
        logger.error(f"❌ File not found: {fnf_error}", exc_info=True)
        raise FileNotFoundError(f"File not found: {csv_path}. Please check the path and try again.")

    except ValueError as v_error:
        logger.error(f"❌ Value error: {v_error}", exc_info=True)
        raise ValueError(f"Value error: {str(v_error)}. Check the CSV file format and ensure all required columns are present.")

    except pd.errors.ParserError as parser_error:
        logger.error(f"❌ CSV parsing error: {parser_error}", exc_info=True)
        raise pd.errors.ParserError("Error parsing CSV file. Please check the file format and content.")

    except Exception as e:
        logger.critical(f"❌ Unexpected error during preprocessing: {e}", exc_info=True)
        raise Exception(f"Unexpected error during preprocessing: {str(e)}")
