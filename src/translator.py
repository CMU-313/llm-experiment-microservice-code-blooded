import os
from ollama import Client
import re

_REFUSAL_RE = re.compile(
    r"\b(i\s+don'?t\s+understand|cannot|can'?t|sorry|unable|refuse|error|invalid|not supported)\b",
    re.IGNORECASE
)
# Initialize Ollama client
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=OLLAMA_HOST)
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


def get_language(post: str) -> str | None:
    context = """\
      You are a language classifier. Detect the language of the input text and reply only with the English name of that language.
      If the input text is malformed or incomprehensible, reply with: "None"\
      """
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": f"Classify the language of this: {post}"
            }
        ]
    )
    return response.message.content


def get_translation(post: str) -> str | None:
    context = """\
      You are a language translator. Translate the text into standard English.
      If it is already in English, return the input text unedited.
      If the input text is malformed or incomprehensible, respond: I don't understand your request

      Example:
      INPUT: Bonjour, je m'appelle Bob
      OUTPUT: Hello, my name is Bob.\
      """
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": f"Translate this: {post}"
            }
        ]
    )
    return response.message.content

def translate_content(post: str) -> tuple[bool, str]:
    fallback = (False, "Something went wrong")
    try:
        language = get_language(post)

        if not language or not isinstance(language, str)  or _REFUSAL_RE.search(language):
            print("Language failed -- returning fallback")
            return fallback

        if language == 'English':
          return (True, post)

        res = get_translation(post)

        if not res or not isinstance(res, str) or _REFUSAL_RE.search(res):
            print("Translation failed -- returning fallback")
            return fallback

        return (False, res)

    except Exception as e:
        print("Exception -- returning fallback")
        return fallback
    

# def translate_content(content: str) -> tuple[bool, str | None]:
#     is_english = True
#     language = get_language(content)

#     if language != 'English':
#         is_english = False

#     translated = get_translation(content)

#     return (is_english, translated)
