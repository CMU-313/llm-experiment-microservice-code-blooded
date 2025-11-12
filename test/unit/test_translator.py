from unittest.mock import Mock, patch
from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    with patch('src.translator.client') as mock_client:
        lang_response = Mock()
        lang_response.message.content = "French"
        
        translation_response = Mock()
        translation_response.message.content = "Hello, my name is Bob"
        
        mock_client.chat.side_effect = [lang_response, translation_response]
        
        is_english, translated = translate_content("Bonjour, je m'appelle Bob")
        
        assert is_english == False
        assert translated == "Hello, my name is Bob"
        assert mock_client.chat.call_count == 2

def test_llm_gibberish_response():
    with patch('src.translator.client') as mock_client:
        lang_response = Mock()
        lang_response.message.content = "I don't understand this text"
        
        mock_client.chat.return_value = lang_response
        
        is_english, translated = translate_content("@#$%^&*()")
        
        assert is_english == False
        assert translated == "Something went wrong"
        # Should only call get_language, not get_translation
        assert mock_client.chat.call_count == 1