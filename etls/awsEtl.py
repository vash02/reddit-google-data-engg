import s3fs
import os
from utils.constants import AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY

def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(anon=False,
                               key= AWS_ACCESS_KEY_ID,
                               secret=AWS_ACCESS_KEY)
        return s3
    except Exception as e:
        print(e)

def create_bucket_if_not_exist(s3: s3fs.S3FileSystem, bucket:str):
    try:
        if not s3.exists(bucket):
            s3.mkdir(bucket)
            print("Bucket created")
        else :
            print("Bucket already exists")
    except Exception as e:
        print(e)


def upload_to_s3(s3: s3fs.S3FileSystem, local_directory: str, bucket: str, s3_folder: str):
    try:
        # List all files in the local directory
        local_files = os.listdir(local_directory)
        print(local_directory)

        # Iterate over each file in the directory and upload to S3
        for local_file in local_files:
            local_file_path = os.path.join(local_directory, local_file)
            s3_file_key = f"{s3_folder}/raw/{local_file}"
            s3.put(local_file_path, f"{bucket}/{s3_file_key}")
            print(f"File '{local_file}' uploaded to S3 as '{s3_file_key}'")
        print("All files uploaded to S3")
    except FileNotFoundError:
        print("One or more files were not found")
