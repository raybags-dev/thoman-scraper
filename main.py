import asyncio
from src.scrappers.scrape_electric_basses import process_endpoints_and_save_base_guitar_data
from src.scrappers.synthesizers import process_endpoints_and_save_synthesizer_data

async def main():
    isGuitarDataCollected = await process_endpoints_and_save_base_guitar_data(run_scraper=False, depth=None)
    isSynthDataCollected = await process_endpoints_and_save_synthesizer_data(run_scraper=False, depth=None)

if __name__ == '__main__':
    asyncio.run(main())
