import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from utils.fs_recorder import write_to_file_handler
from middleware.logger.logger import initialize_logging, my_log
from middleware.errors.error_handler import handle_exceptions

initialize_logging()


def create_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S')
@handle_exceptions
async def parse_and_save_data(page_content: str, data_file: str):
    if not page_content:
        my_log(message="Page content is null or empty, skipping parsing.", log_type="warn")
        return

    soup = BeautifulSoup(page_content, 'html.parser')
    product_listings = soup.find_all('div', class_='fx-product-list-entry')
    data = []

    for product in product_listings:
        try:
            product_id = product.get('id')
            product_details = product.find('div', class_='product__title fx-text')
            manufacturer = product_details.find('span', class_='title__manufacturer').text.strip()
            name = product_details.find('span', class_='title__name').text.strip()
            rating_stars = product.find('div', class_='fx-rating-stars__filler')
            rating_percentage = rating_stars['style'] if rating_stars else 'width:0%'
            rating_value_str = rating_percentage.split(':')[1].replace('%', '').strip('; ')
            rating_value = float(rating_value_str) / 20
            rating_count_element = product.find('div', class_='fx-rating-stars__description')
            rating_count = rating_count_element.text.strip() if rating_count_element else None
            description_items = product.find_all('li',
                                                 class_='product__description-item fx-list__item fx-list__item--circle')
            description = '; '.join([item.text.strip() for item in description_items])
            availability = product.find('span', class_='fx-availability').text.strip()
            price = product.find('span',
                                 class_='fx-typography-price-primary fx-price-group__primary product__price-primary').text.strip()

            data.append({
                'Product ID': product_id,
                'Manufacturer': manufacturer,
                'Name': name,
                'Rating': rating_value,
                'Review Count': rating_count,
                'Description': description,
                'Availability': availability,
                'Price': price,
                'createdAt': create_timestamp()
            })
        except AttributeError as e:
            if "'NoneType' object has no attribute 'text'" in str(e):
                my_log(message=f"Error processing product: {e}", log_type="warn")
                continue
            else:
                raise

    write_to_file_handler(data_file, data)

    my_log(message=f"Parsed data saved to {data_file}", log_type="info")
    return True
