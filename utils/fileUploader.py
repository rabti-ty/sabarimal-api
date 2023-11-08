import boto3
from botocore.exceptions import NoCredentialsError
import json
from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')

region_name = configur.get('sabrimala_qr_s3','REGION')
aws_access_key = configur.get('sabrimala_qr_s3','ACCESS_KEY')
aws_secret_access_key =  configur.get('sabrimala_qr_s3','SECRET_KEY') 
bucket_name = configur.get('sabrimala_qr_s3','BUCKET_NAME')
local_dir = configur.get('sabrimala_qr_s3','LOCAL_DIR')

def get_s3_client():
    s3_client = boto3.client(
        's3',
        region_name=region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key
    )
    return s3_client

def upload_to_aws(local_file_name):
    s3 = get_s3_client()
    local_file_uri = local_dir+"/"+local_file_name
    try:
        s3.upload_file(local_file_uri,bucket_name,local_file_name)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True