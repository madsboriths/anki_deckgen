import requests

WIKIPEDIA_SUMMARY_ENDPOINT = (
    "https://en.wikipedia.org/wiki/{title}"
)

class Retrieval:
    def __init__(self, topic: str, description: str):
        self.title = topic
        self.description = description