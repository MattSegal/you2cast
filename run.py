import yaml

from storage import upload_fileobj_mp3, list_fileobjs
from youtube import download_youtube
from podcast import update_podcast
import secrets

def main():
    with open('videos.yaml', 'r') as f:
        videos = yaml.safe_load(f)

    print('\nChecking for existing files')    
    existing_fileobjs = list_fileobjs()
    existing_file_names = set([o['file_name'] for o in existing_fileobjs])

    print('Ensuring all videos are uploaded')
    for video in videos:
        file_name = get_file_name(video['key'])
        if file_name in existing_file_names:
            print(f'Skipping {file_name} - already uploaded')
            continue
        else:
            url = get_youtube_url(video['key'] )
            youtube_info = download_youtube(url)
            file_name = get_file_name(video['key'])
            print(f'Uploading {file_name} to S3')
            with open(file_name, 'rb') as f:
                upload_fileobj_mp3(f, file_name)

    print('\nRefreshing list of existing files')    
    fileobj_lookup = {
        obj['file_name']: obj
        for obj in list_fileobjs()
    }
    print('\nUpdating podcast')    
    podcast_videos = []
    for video in videos:
        file_name = get_file_name(video['key'])
        s3_obj = fileobj_lookup[file_name]
        url = get_youtube_url(video['key'] )
        youtube_info = download_youtube(url, download=False)
        podcast_videos.append({
            'title': video.get('title', youtube_info['title']),
            'description': video.get('description', youtube_info['description']),
            'modified_at': s3_obj['modified_at'],
            'url': url,
            'audio_url': get_s3_url(video['key']),
            'audio_size': s3_obj['size'],
        })

    update_podcast(podcast_videos)


def get_s3_url(key):
    return f'https://s3-ap-southeast-2.amazonaws.com/{secrets.S3_BUCKET}/media/{key}.mp3'


def get_youtube_url(key):
    return 'https://www.youtube.com/watch?v=' + key


def get_file_name(s):
    return s + '.mp3'


if __name__ == '__main__':
    main()