from io import BytesIO

from feedgen.feed import FeedGenerator

from storage import upload_podcast

def update_podcast(videos):
    gen = FeedGenerator()
    # Add general meta info
    gen.load_extension('podcast')
    gen.title('Matt\'s YouTube')
    gen.description('Matt\'s YouTube playlist.')
    gen.language('en')
    gen.author({'name': 'Matt Segal', 'email': 'mattdsegal@gmail.com'})
    gen.webMaster('mattdsegal@gmail.com')
    gen.ttl(24 * 60 * 60)  # Minutes
    gen.link({'href': 'hhttps://mattsegal.github.io'})

    # Add info for each video
    for video in videos:
        entry = gen.add_entry()
        entry.id(video['url'])
        entry.enclosure(video['audio_url'], str(video['audio_size']), 'audio/mpeg')
        entry.title(video['title'])
        entry.link({'href': video['url']})
        entry.ttl(24 * 60 * 60)  # Minutes
        entry.published(video['modified_at'])
        entry.description(video['description'])

    # Upload to S3
    text_buffer = BytesIO()
    gen.rss_file(text_buffer)
    upload_podcast(text_buffer)
    