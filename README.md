# You2Cast

Python script for turning YouTube videos (listed in `videos.yml`) into a podcast.

## How to use

Edit `videos.yml` to contain all the YouTube videos you want to listen to.

Create a `secrets.py` file with your AWS credentials and your S3 bucket 

```
AWS_ACCESS_KEY_ID = 'XXX'
AWS_SECRET_ACCESS_KEY = 'XXX'
S3_BUCKET = 'your-s3-bucket'
```

Install Python packages

```
pip3 install -r requirements.txt
```

Run the script

```
python3 run.py
```
