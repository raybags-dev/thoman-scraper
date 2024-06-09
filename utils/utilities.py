import re
import aiohttp
import asyncio
from dataclasses import dataclass
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from utils.fs_recorder import write_to_file_handler
from middleware.errors.error_handler import handle_exceptions
from middleware.logger.logger import initialize_logging, my_log


initialize_logging()

@dataclass
class PageEndpoints:
    base_url: str
    total_products: int
    products_per_page: int = 25

    def generate_endpoints(self):
        my_log(message=f"Generating endpoints with base_url={self.base_url}, total_products={self.total_products}, "
                       f"products_per_page={self.products_per_page}", log_type="info")
        total_pages = (self.total_products + self.products_per_page - 1) // self.products_per_page
        endpoints = [f"{self.base_url}?ls=25&pg={page}" for page in range(1, total_pages + 1)]
        my_log(message=f"Generated endpoints: {endpoints}", log_type="info")
        return endpoints
@handle_exceptions
async def fetch_page_content(url: str, retries: int = 3, delay: int = 5) -> str:
    my_log(message=f"Fetching content from URL: {url}", log_type="info")

    attempt = 0
    while attempt < retries:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Set a timeout for the page navigation
                page.set_default_timeout(60000)

                # Navigate to the URL
                await page.goto(url, timeout=60000)

                await page.wait_for_load_state("networkidle", timeout=10000)  # Increase timeout to 10 seconds

                # Get page content
                page_content = await page.content()

                # Close the browser
                await browser.close()

                if page_content:
                    my_log(message="Fetched page content...", log_type="info")
                    return page_content
                else:
                    raise ValueError("Empty page content")

        except PlaywrightTimeoutError as e:
            my_log(message=f"Timeout error fetching page content on attempt {attempt + 1}: {str(e)}", log_type="warn")
        except Exception as e:
            my_log(message=f"Error fetching page content on attempt {attempt + 1}: {str(e)}", log_type="warn")

        attempt += 1
        if attempt < retries:
            my_log(message=f"Retrying in {delay} seconds...", log_type="info")
            await asyncio.sleep(delay)
        else:
            my_log(message="Max retries reached. Skipping this URL.", log_type="warn")

    return ""
def extract_total_product_count(html: str) -> int:
    my_log(message="Extracting total products from HTML content", log_type="info")
    regex_patterns = [
        r'"result_count":(\d+)',
        r'"cumulative_result_count":(\d+)',
        r'"resultCount":(\d+)',
        r'"cumulativeResultCount":(\d+)'
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, html)
        if match:
            total_product_count = int(match.group(1))
            my_log(message=f"Total products found: {total_product_count} using pattern: {pattern}", log_type="info")
            return total_product_count

    my_log(message="Could not find the product count in the HTML content.", log_type="error")
    raise ValueError("Could not find the product count in the HTML content.")
@handle_exceptions
async def main_paginator(product_endpoint: str, product_filepath: str) -> bool:
    my_log(message=f"Fetching content from {product_endpoint}", log_type="info")
    page_content = await fetch_page_content(product_endpoint)

    try:
        if page_content is None:
            my_log(message="Failed to fetch page content.", log_type="error")
            return False

        total_products = extract_total_product_count(page_content)
        page_endpoints = PageEndpoints(base_url=product_endpoint.split('?')[0], total_products=total_products)
        endpoints = page_endpoints.generate_endpoints()

        # Step 4: Write endpoints to the CSV file
        write_to_file_handler(filepath=product_filepath, results=[{'endpoint': ep} for ep in endpoints])
        my_log(message=f"Total number of entries collected: {len(endpoints)}", log_type="info")

        return len(endpoints) > 0

    except Exception as e:
        my_log(message=f"Error in bass_paginator: {e}", log_type="error")
        return False
