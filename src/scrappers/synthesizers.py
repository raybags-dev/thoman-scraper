import pandas as pd
import asyncio
from pathlib import Path
from utils.utilities import main_paginator, fetch_page_content
from utils.parse_data import parse_and_save_data
from middleware.logger.logger import initialize_logging, my_log
from middleware.errors.error_handler import handle_exceptions
import validators
from utils.clear_files import clear_files

initialize_logging()


@handle_exceptions
async def process_endpoints_and_save_synthesizer_data(run_scraper: bool = None, depth: int = None):
    synthesizer_base_url = "https://www.thomann.de/gb/all-products-from-the-category-acoustic-drums.html"
    synthesizer_endpoints_file_path = "src/endpoints/synthesizer_endpoints/synthesizer_endpoints.csv"
    parsed_data_synth_file_path = "src/data/parsed_synthesizer_data.csv"

    if run_scraper:
        clear_files(synthesizer_endpoints_file_path, parsed_data_synth_file_path)

    # If run_scraper is explicitly set to False, skip the entire scraping process
    if run_scraper is False:
        my_log(message="run_scraper is set to False. Skipping the scraping process.", log_type="info")
        return False

    # Check if endpoints file exists and is not empty
    if not Path(synthesizer_endpoints_file_path).is_file() or Path(synthesizer_endpoints_file_path).stat().st_size == 0:
        my_log(message="Endpoints file does not exist or is empty. Generating new endpoints.", log_type="info")
        run_scraper = await main_paginator(synthesizer_base_url, synthesizer_endpoints_file_path)
        if not run_scraper:
            my_log(message="Failed to generate endpoints. Exiting.", log_type="error")
            return False
    else:
        run_scraper = True

    # Load endpoints from file
    try:
        endpoints_df = pd.read_csv(synthesizer_endpoints_file_path)
        if endpoints_df.empty:
            raise ValueError("Endpoints file is empty")
    except (pd.errors.EmptyDataError, ValueError) as e:
        my_log(message=f"Error reading endpoints file: {str(e)}. Exiting.", log_type="error")
        return False

    endpoints = endpoints_df['endpoint'].tolist()

    # Validate URLs
    endpoints = [url for url in endpoints if validators.url(url)]
    if not endpoints:
        my_log(message="No valid endpoints found. Exiting.", log_type="error")
        return False

    # Limit the number of endpoints to process if depth is specified
    if depth is not None and depth > 0:
        endpoints = endpoints[:depth]

    my_log(message=f"Processing {len(endpoints)} endpoints", log_type="info")

    async def process_endpoint(endpoint):
        try:
            content = await fetch_page_content(endpoint)
            if content:
                await parse_and_save_data(page_content=content, data_file=parsed_data_synth_file_path)
        except Exception as e:
            my_log(message=f"Error processing endpoint {endpoint}: {str(e)}", log_type="error")

    # Limit concurrency to process 10 endpoints at a time
    semaphore = asyncio.Semaphore(10)

    async def limited_task(endpoint):
        async with semaphore:
            await process_endpoint(endpoint)

    await asyncio.gather(*(limited_task(endpoint) for endpoint in endpoints))

    return True