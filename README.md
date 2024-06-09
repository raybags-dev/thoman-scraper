# Thomann Scraper

Thomann Scraper is a Python-based web scraping tool designed to collect data from the Thomann website for a specified category of products. It allows users to scrape product information such as prices, descriptions, and reviews.

## Features

- **Scraping Endpoints**: The scraper generates endpoints for a specified category of products on the Thomann website.
- **Fetching Page Content**: It fetches the HTML content of each endpoint asynchronously using `asyncio` and `aiohttp`.
- **Parsing and Saving Data**: The scraped data is parsed and saved into CSV files for further analysis.
- Supports retry logic and logging for robust scraping.
- **Error Handling**: The scraper includes error handling mechanisms to deal with exceptions that may occur during scraping.
- **Logging**: Detailed logging is implemented to track the scraping process and any encountered errors.

## Installation

1. Clone the repository:

```sh
  git clone https://github.com/raybags-dev/thoman-scraper.git
```
```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```

1. Install dependencies:
```sh
    pip install -r requirements.txt
    playwright install
```
```sh
    python main.py
```
2. Set up configuration:

- Configure the scraping parameters in `config.py`.
- Customize logging settings in `middleware/logger/logger.py`.

## Usage

1. Run the main script:
2. Monitor the scraping process through console logs.

## Contributing
Contributions are welcome - especially about the below improvement suggestions! Please feel free to open an issue or submit a pull request.

## Improvements

- **Logging**: The logging system in Thomann Scraper can be enhanced to integrate with external monitoring platforms like Kibana or Elasticsearch. By default, the scraper logs information, warnings, and errors to the console. However, to integrate with external monitoring platforms, you can make the following improvements:
    - Configure Logging Handlers: Implement additional logging handlers such as SysLogHandler or HTTPHandler to send logs to remote servers. These handlers can be configured to send logs to external services like Kibana or Elasticsearch.
    - Enhance Log Formatting: Customize log formatting to include additional metadata such as timestamps, log levels, and source information. This ensures that logs are structured and standardized for better analysis and monitoring.
    - Centralized Logging: Implement centralized logging solutions such as Fluentd or Logstash to aggregate logs from multiple instances of the scraper. This allows for centralized log storage and analysis, facilitating troubleshooting and monitoring across distributed environments.
- **Data handling**: Thomann Scraper currently saves scraped data to CSV files locally. However, there are opportunities to improve data handling capabilities, including:
    - Database Integration: Instead of storing data in CSV files, integrate the scraper with relational or NoSQL databases such as MySQL, PostgreSQL, MongoDB, or Firebase. This enables efficient data storage, retrieval, and querying, making it easier to manage large datasets.
    - Streaming Data Pipelines: Implement data streaming pipelines using technologies like Apache Kafka or Apache Beam. This allows real-time processing and analysis of scraped data, enabling immediate insights and actions based on incoming data streams.
    - Message Queue Integration: Utilize message queue systems such as RabbitMQ or Apache ActiveMQ to decouple data ingestion from processing. This improves scalability and fault tolerance by distributing data processing tasks across multiple workers.
- **Storage Improvements**: Thomann Scraper can be enhanced to support various storage options beyond local file storage. Consider the following improvements:
    - Cloud Storage Integration:  Integrate the scraper with cloud storage services such as Google Cloud Storage (GCS), Amazon S3, or Microsoft Azure Blob Storage. This allows seamless storage and retrieval of scraped data in scalable and durable cloud environments.
    - Object Storage APIs:  Utilize object storage APIs provided by cloud providers to directly upload scraped data to cloud storage buckets. This eliminates the need for intermediate local storage and improves data transfer efficiency.
    - Data Lake Architectures: Implement data lake architectures using technologies like Apache Hadoop or AWS Glue. This enables storing large volumes of structured and unstructured data in a cost-effective manner, facilitating data analysis and machine learning tasks.

