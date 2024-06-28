import openai
from django.conf import settings

EMBEDDING_MODEL = "text-embedding-ada-002"


def get_embedding(text: str):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(
        input = [text],
        model = EMBEDDING_MODEL,
        api_key = settings.OPENAI_API_KEY,
    )
    return response["data"][0]["embedding"]