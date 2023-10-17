def youtube_url_to_embed(youtube_url):
    youtube_format = "-"
    if youtube_url is not None:
        youtube_format = youtube_url\
            .replace("youtu.be/", "www.youtube.com/embed/")\
            .replace("watch?v=", "embed/")

    return youtube_format
