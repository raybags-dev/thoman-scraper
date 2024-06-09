import pandas as pd
from pathlib import Path
from middleware.errors.error_handler import handle_exceptions


@handle_exceptions
def write_to_file_handler(filepath, results, chunksize=100) -> None:
    # Ensure the directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    if not results:
        with open(filepath, 'a') as f:
            f.write("Operation completed - no data returned.\n")
        print(f"Transaction completed { filepath }")
        return

    # Check if the file already exists and is not empty
    file_exists = Path(filepath).is_file() and Path(filepath).stat().st_size > 0

    # Create a DataFrame iterator for chunked processing
    df_iter = pd.DataFrame(results).groupby(lambda x: x // chunksize)

    # Write DataFrame chunks to file
    with open(filepath, 'a') as f:
        for i, chunk in df_iter:
            chunk.to_csv(f, header=not file_exists and i == 0, index=False)
            file_exists = True  # Ensure subsequent chunks do not write headers
            print(f"Chunk { i + 1 } written to { filepath }")