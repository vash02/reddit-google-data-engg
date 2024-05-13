import pandas as pd
from utils.constants import GOOGLE_API_KEY, GOOGLE_CX, OUTPUT_PATH

from etls.customSearchEtl import search_reddit_subreddit, process_subreddit_search, load_data_to_csv


def custom_search_pipeline(file_name: str,query: str, subreddit: str):
    # connecting to reddit instance
    search_data = search_reddit_subreddit(query, subreddit, GOOGLE_API_KEY, GOOGLE_CX)
    # transform
    processed_data = process_subreddit_search(search_data)
    # print(type(processed_data))
    search_df = pd.DataFrame(processed_data)

    # loading to csv
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    load_data_to_csv(search_df, file_path)

    return OUTPUT_PATH
