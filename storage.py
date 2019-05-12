import boto3

import secrets

mp3_upload_config = {
    'ContentType': 'audio/mpeg',
    'ACL': 'public-read'
}
client = boto3.Session(
    region_name='ap-southeast-2',
    aws_access_key_id=secrets.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=secrets.AWS_SECRET_ACCESS_KEY,
).client('s3')

def upload_podcast(f):
    f.seek(0)
    s3_key = 'podcast.xml'
    upload_config = {
        'ContentType': 'application/xml',
        'ACL': 'public-read'
    }
    client.upload_fileobj(f, secrets.S3_BUCKET, s3_key, upload_config)


def upload_fileobj_mp3(f, file_name):
    key = f'media/{file_name}'
    client.upload_fileobj(f, secrets.S3_BUCKET, key, mp3_upload_config)


def list_fileobjs():
    response = client.list_objects(Bucket=secrets.S3_BUCKET, Prefix='media/')
    return [
        {
            'file_name': obj['Key'].replace('media/', ''),
            'modified_at': obj['LastModified'],
            'size': obj['Size'],
        }
        for obj in response.get('Contents', [])
        if obj['Key'].replace('media/', '')
    ]