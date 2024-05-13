import json

import requests
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import StringType, StructType, StructField, ArrayType
def search_reddit_subreddit(query, subreddit, api_key, cx):
    """
    Perform a Google Custom Search API request to search for results related to a specific subreddit.

    Args:
        query (str): The search query.
        subreddit (str): The subreddit to restrict the search to (e.g., "reddit.com/r/<subreddit>").
        api_key (str): Your Google API key with access to the Custom Search API.
        cx (str): Your Custom Search Engine ID (CSE ID).

    Returns:
        list: A list of search result items (dict).
    """
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "siteSearch": subreddit  # Restrict search to specific subreddit
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    # data = response.json()
    data = json.loads(response.content.decode("utf"))
    # keys_list = list(data.keys())
    # print(keys_list)
    # print(data['kind'])
    # print(data['queries'])#['request'][0]['searchTerms'])
    # print(data['items'])
    # print(data)
    return data

def process_subreddit_search(data):
    # print(type(data))
    processed_data = {
        'kind': data['kind'],
        'searchTerms': data['queries']['request'][0]['searchTerms'],
        'items': [
            {
                'title': item['title'],
                'link': item['link'],
                'snippet': item['snippet']
            }
            for item in data['items']
        ]
    }
    # print(processed_data)

    return processed_data

def load_data_to_json(data, path):
    spark = SparkSession.builder \
        .appName("Save DataFrame to json") \
        .getOrCreate()

    schema = StructType([
        StructField("kind", StringType(), True),
        StructField("searchTerms", StringType(), True),
        StructField("items", ArrayType(
            StructType([
                StructField("title", StringType(), True),
                StructField("link", StringType(), True),
                StructField("snippet", StringType(), True)
            ])
        ), True)
    ])

    # Create DataFrame from JSON data using the defined schema
    df = spark.createDataFrame([data], schema=schema)
    df = df.withColumn('id', monotonically_increasing_id())
    df.coalesce(1).write.mode("overwrite").json(path)

    spark.stop()



def load_data_to_parquet(data: pd.DataFrame, path: str):
    spark = SparkSession.builder \
        .appName("Save DataFrame to Parquet") \
        .getOrCreate()
    spark_df = spark.createDataFrame(data)
    print(spark_df.schema)


    try:
        # Write DataFrame to Parquet format
        spark_df.coalesce(1).write.mode("overwrite").parquet(path)
        print(f"DataFrame saved as Parquet file: {path}")
    except Exception as e:
        print(f"Error occurred while saving DataFrame to Parquet: {e}")
    finally:
        # Stop Spark session
        spark.stop()


data = search_reddit_subreddit("data engineering","reddit.com/r/dataengineering","AIzaSyABGdVM83A28q2Xecz2e6sKuBDjINnpgSg","7028cb91469b0412d")

processed_data = process_subreddit_search(data)
load_data_to_json(pd.DataFrame(processed_data),"data/output/reddit_search_20240429.json")