import os
import boto3
import zipfile

s3_client = boto3.client('s3')

def handler(event, context):
    for record in event[
        'Records']:  # For each record in this event that was sent from the bucket (ATM uploading images to a bucket)
        invoking_bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    print('key: %s'%(key))
    key_end = key.split('/').pop()
    local_input_path = '/tmp/input-%s'%(key_end)  # Generate a temporary input path (from a random universally unique identifier and the key allowing for multiple same-named input files)
    print('local_input_path: %s'%(local_input_path))
    local_output_path = '/tmp/output-%s.zip' % (key_end)
    s3_client.download_file(invoking_bucket, key, local_input_path)
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED
    print ('creating archive')
    zf = zipfile.ZipFile(local_output_path, mode='w')
    try:
        print ('adding local_input_path')
        zf.write(local_input_path,compress_type=compression)
    finally:
        print ('closing')
        zf.close()
    print(zf.infolist())
    s3_client.upload_file(local_output_path, invoking_bucket, '%s.zip'%(key),ExtraArgs={'ACL': 'public-read'})
