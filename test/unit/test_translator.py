from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    is_english, translated = translate_content("Bonjour, je m'appelle Bob")
    assert is_english == False
    assert translated != "Something went wrong"
    assert len(translated) > 0

def test_llm_gibberish_response():
    is_english, translated = translate_content("@#$%^&*()")
    assert is_english == False
    assert len(translated) > 0