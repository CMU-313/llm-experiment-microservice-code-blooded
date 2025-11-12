from src.translator import translate_content


# def test_chinese():
#     is_english, translated_content = translate_content("这是一条中文消息")
#     assert is_english == False
#     assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    is_english, translated_content = translate_content("Hola, cómo estás")
    assert is_english == False
    assert translated_content == "Hello, how are you?"

# returns error message if the input is not recognizable
def test_llm_gibberish_response():
    is_english, translated_content = translate_content("fjsefsf geiofensl")
    assert is_english == False
    assert translated_content == "Something went wrong"