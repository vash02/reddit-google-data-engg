# Reddit-Google API Data Engineering Pipeline

## Architecture
![projectArch](https://github.com/vash02/reddit-google-data-engg/assets/31550732/7e50836a-45c6-4646-8cee-4a479a0e26a1)

1. Data Sources: Reddit and google APIs
2. Pipeline Scheuler: Apahe Airflow
3. Raw Data Cloud Storage: Amazon S3
4. Data Cataloging and ETL jobs: AWS Glue
5. Data Querying and Analytics: Amazon Athena
6. NoSQL database: DynamoDB

## Prerequisites
1. Reddit and Google custom search API credentials
2. AWS S3 account and credentials, also access roles added for IAM user.
3. Docker installed
4. Python 3.9
5. Packages in requirements.txt
6. Pycharm or any Python IDE

## Steps to Run
1. Clone the repository
2. Open the project in IDE and execute the command
```bash
pip install -r requirements.txt
```
3.The, execute the following command to start the docker conatiners
```bash 
docker compose up -d --build
```
4. Launch the airflow web UI to view the and trigger the pipeline via scheduler
```bash
localhost:8080/home
```
5. Once the pipeline run succeeds you will be able to see data uploaded ins3 buckets.
6. Run Glue jobs to transform the data and create tables using Athena from transformed data to run queries.
7. Create table importing unstructured directory csv data in DynamoDB

## Preprocessed Data Schemas

### Preprocessed Reddit Data Schema
- **id**: string (Primary Key)
- **title**: string
- **score**: int
- **selftext**: string
- **num_comments**: int
- **author**: string
- **created_utc**: timestamp
- **url**: string
- **over_18**: boolean
- **edited**: boolean
- **spoiler**: boolean
- **stickied**: boolean

### Preprocessed Google Search Data Schema
- **id**: int (Primary Key)
- **kind**: string
- **searchterms**: string
- **items**: map<string, string>

## Schemas/Metadata for tables created in Athena

### reddit_post (reddit_data_table)
- **id**: string (Primary Key)
- **title**: string
- **selftext**: string
- **score**: int
- **num_comments**: int
- **author**: string
- **created_utc**: date/time
- **url**: string
- **over_18**: boolean
- **edited**: boolean
- **spoiler**: boolean
- **stickied**: boolean

### search_data (search_data_table)
- **id**: int (Primary Key)
- **kind**: string
- **searchterms**: string
- **items**: map<string, string>

### search_keyword (search_keywords_data)
- **id**: string (Primary Key)
- **title**: string
- **link**: string
- **keyword_1**: string
- **keyword_2**: string
- **keyword_3**: string
- **cleaned_snippet**: string

### transformed_post (transformed)
- **id**: string (Primary Key)
- **title**: string
- **score**: bigint
- **num_comments**: bigint
- **author**: string
- **created_utc**: string
- **url**: string
- **over_18**: boolean
- **ess_combined**: string

### subreddit_search_data
- **kind**: string
- **searchterms**: string
- **items**: string

## References:
1. https://github.com/airscholar/RedditDataEngineering
2. https://www.reddit.com/wiki/api/
3. https://developers.google.com/custom-search/v1/overview
4. https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html
5. https://docs.aws.amazon.com/athena/latest/ug/using-athena-sql.html
6. https://docs.aws.amazon.com/dynamodb/
