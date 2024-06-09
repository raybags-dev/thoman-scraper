import pandas as pd
from pathlib import Path
from typing import List, Dict
from middleware.errors.error_handler import handle_exceptions


@handle_exceptions
def write_to_file_handler(filepath: str, results: List[Dict], chunksize: int = 100) -> None:
    """
    Write results to a file in chunks of 10.

    Args:
        filepath (str): Path to the output file.
        results (List[Dict]): List of dictionaries representing the data.
        chunksize (int): Number of rows per chunk.
    """
    # Ensure the directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    if not results:
        with open(filepath, 'a') as f:
            f.write("Operation completed - no data returned.\n")
        print(f"Transaction completed {filepath}")
        return

    # Check if the file already exists and is not empty
    file_exists = Path(filepath).is_file() and Path(filepath).stat().st_size > 0

    # Create a DataFrame from the results
    df = pd.DataFrame(results)

    # Split the DataFrame into chunks and write to file
    with open(filepath, 'a') as f:
        for i in range(0, len(df), chunksize):
            chunk = df.iloc[i:i + chunksize]
            chunk.to_csv(f, header=not file_exists and i == 0, index=False)
            file_exists = True
            print(f"Chunk {(i // chunksize) + 1} written to {filepath}")

