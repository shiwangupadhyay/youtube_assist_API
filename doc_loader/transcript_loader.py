from langchain_community.document_loaders import YoutubeLoader

def transcript_loader(url : str) -> str:
    """
    Download the transcript of the Video.
    Supports Multiple Language.

    Args:
        URL of the Video.
    Returns:
        Transcript of the video.
    """
    loader = YoutubeLoader.from_youtube_url(
                url,
                language=["en", "hi"]
            )
    docs = loader.load()
    return docs