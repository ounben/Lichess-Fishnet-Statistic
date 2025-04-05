# Lichess Fishnet Stats Collector

This Python script collects statistics from the Lichess website and Fishnet system, storing them in a CSV file.

## Features

* Collects the number of players and games on Lichess.
* Gathers Fishnet statistics (user and system-related data).
* Reads additional Fishnet statistics from a local file (`.fishnet-stats`).
* Stores all data in a timestamped CSV file.
* Handles errors during data retrieval and parsing.
* Implements exponential backoff for 429 errors (too many requests).

## Prerequisites

* Python 3.x
* The following Python libraries:
    * `requests`
    * `csv`
    * `datetime`
    * `re`
    * `json`

## Installation

1.  Clone the repository:

    ```bash
    git clone [REPOSITORY_URL]
    cd [REPOSITORY_NAME]
    ```

2.  Install the required Python libraries:

    ```bash
    pip install requests
    ```

## Usage

1.  Ensure the `.fishnet-stats` file is in the same directory as the script, or adjust the path in the `read_fishnet_stats()` function.
2.  Run the script:

    ```bash
    python lichess_stats.py
    ```

3.  The statistics will be stored in the `lichess_stats.csv` file.

## CSV File

The CSV file contains the following columns:

* `Timestamp`: The timestamp of the data collection.
* `Spieler`: The number of current players on Lichess.
* `Spiele`: The number of current games on Lichess.
* `Fishnet_User_Acquired`: The number of user-requested analyses.
* `Fishnet_User_Queued`: The number of user analyses in the queue.
* `Fishnet_User_Oldest`: The age of the oldest user analysis in the queue.
* `Fishnet_System_Acquired`: The number of system-requested analyses.
* `Fishnet_System_Queued`: The number of system analyses in the queue.
* `Fishnet_System_Oldest`: The age of the oldest system analysis in the queue.
* `Total_Batches`: The total number of Fishnet batches (from the local file).
* `Total_Positions`: The total number of Fishnet positions (from the local file).
* `Total_Nodes`: The total number of Fishnet nodes (from the local file).

## Error Handling

The script handles the following errors:

* `requests.exceptions.RequestException`: Errors retrieving data from the Lichess website.
* `ValueError`, `AttributeError`, `IndexError`, `json.JSONDecodeError`: Errors parsing data.
* 429 errors (too many requests): The script implements exponential backoff to avoid overloading the server.

## Logging

The script also outputs messages to the console to indicate progress and any errors. For more comprehensive logging, you can use the `logging` module in Python.

## Configuration

* The wait times and the file path for the `.fishnet-stats` file can be adjusted within the script.

## Contributing

Contributions are welcome! Please submit pull requests to fix bugs or add new features.

## License

[Your License]
