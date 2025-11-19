import requests
from abc import ABC, abstractmethod
from typing import Dict

class BaseTranslator(ABC):
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        pass

class EchoTranslator(BaseTranslator):
    """
    A simple translator for testing purposes. It returns the original text,
    prefixed with the language codes.
    """
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        return f"[{source_lang} -> {target_lang}] {text}"

class DeepLTranslator(BaseTranslator):
    """
    A translator using the DeepL API.
    Requires an API key to be set in the config.
    """
    def __init__(self, api_key: str, is_free_api: bool = True):
        self.api_key = api_key
        self.api_url = "https://api-free.deepl.com/v2/translate" if is_free_api else "https://api.deepl.com/v2/translate"

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not self.api_key:
            raise ValueError("DeepL API key is not provided.")

        payload = {
            "auth_key": self.api_key,
            "text": text,
            "source_lang": source_lang.upper(),
            "target_lang": target_lang.upper(),
        }

        try:
            response = requests.post(self.api_url, data=payload)
            response.raise_for_status()
            result = response.json()
            return result['translations'][0]['text']
        except requests.exceptions.RequestException as e:
            print(f"Error calling DeepL API: {e}")
            return f"[API Error] {text}"
        except (KeyError, IndexError):
            print(f"Error parsing DeepL API response: {response.text}")
            return f"[API Error] {text}"


class TranslationEngine:
    """
    Manages different translation providers.
    """
    def __init__(self, config: Dict):
        self.config = config.get('translator', {})
        self.provider_name = self.config.get('provider', 'echo')
        self.translator = self._get_translator()

    def _get_translator(self) -> BaseTranslator:
        if self.provider_name == 'deepl':
            api_key = self.config.get('api_key')
            if not api_key:
                print("Warning: DeepL provider selected but no api_key found in config. Falling back to echo.")
                return EchoTranslator()
            is_free = self.config.get('free_api', True)
            return DeepLTranslator(api_key=api_key, is_free_api=is_free)
        
        # Default to echo translator
        return EchoTranslator()

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        return self.translator.translate(text, source_lang, target_lang)

if __name__ == '__main__':
    # Example usage:
    # To test, you would create a dummy config dict.
    dummy_config = {
        'translator': {
            'provider': 'echo' # or 'deepl', if you have an API key
            # 'api_key': 'YOUR_DEEPL_API_KEY_HERE' 
        }
    }
    
    engine = TranslationEngine(dummy_config)
    translated_text = engine.translate("안녕하세요, 세상!", source_lang="ko", target_lang="en")
    print(f"Translation result: {translated_text}")
