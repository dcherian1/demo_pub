import pandas as pd
import boto3
import time
from botocore.exceptions import ClientError
from io import StringIO 

# Specify the bucket name and file key (path)
input_bucket_name = 'adp-eu-west-1-101965541725-dev2-dlz'
input_file_key = 'fisheries_wdfwraw/wa_salmon_species_population/'
output_bucket_name = 'adp-eu-west-1-101965541725-dev2-lz'
output_file_key = 'fisheries_wdfwraw/wa_salmon_species_population_processed'
user = 'williammiller'
file_type = 'csv'
file_name = "processed"
upload_date = str(int(time.time()))
prefix = "/".join([output_file_key, "upload_date=" + upload_date, user, file_type, file_name])

# Initialize the S3 client
s3 = boto3.client('s3')

file = s3.list_objects_v2(Bucket= input_bucket_name, Prefix = input_file_key)['Contents'][0]
key = file.get('Key')
print(key)
object = s3.get_object(Bucket=input_bucket_name,Key=key)
data = object['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(data))
df.shape

df2 = df.dropna(how='any')
df2.shape

bytes_to_write = df2.to_csv(index=False, header=True, sep=',', encoding='utf-8')
s3.put_object(Bucket=output_bucket_name, Key=prefix, Body=bytes_to_write.encode('utf-8'))

print ("Git test")
