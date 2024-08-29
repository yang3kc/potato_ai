# POTATO (Panel-based Open Term-level Aggregate Twitter Observatory)

POTATO is a prototype website that uses data from the Lazer Lab's Twitter Panel to analyze tweets and provide aggregate information about people who tweeted about specific terms.

## System Overview

POTATO uses the following technologies:
- Docker and Docker Compose for containerization
- MongoDB for data storage
- Flask for the API
- Python for data processing and analysis

## Setup and Installation

1. Ensure you have Docker and Docker Compose installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/your-username/potato_ai.git
   cd potato_ai
   ```

3. Place your TSV file(s) containing tweet data in the project directory.

4. Update the file path in `ingestion/ingest.py` to point to your TSV file:
   ```python
   if __name__ == "__main__":
       ingest_data("path_to_your_tsv_file.tsv")
   ```

5. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

6. In a separate terminal, run the data ingestion script:
   ```
   docker-compose exec api python -m ingestion.ingest
   ```

## Usage

Once the system is set up and data is ingested, you can query the API using the following endpoints:

1. Overall search statistics:
   ```
   GET http://localhost:5000/search?term=<search_term>
   ```
   This returns overall statistics for tweets containing the search term, including:
   - Total tweet count
   - Number of unique users
   - Average number of likes
   - List of place IDs

2. Daily tweet counts:
   ```
   GET http://localhost:5000/search/daily?term=<search_term>
   ```
   This returns the number of tweets containing the search term for each day.
