from etls.awsEtl import connect_to_s3, create_bucket_if_not_exist, upload_to_s3
from utils.constants import AWS_BUCKET_NAME


def upload_s3_pipeline(ti):
    dir_path = ti.xcom_pull(task_ids='reddit_api_extraction', key='return_value')

    s3 = connect_to_s3()
    create_bucket_if_not_exist(s3, AWS_BUCKET_NAME)
    upload_to_s3(s3, dir_path, AWS_BUCKET_NAME, dir_path.split('/')[-1])


