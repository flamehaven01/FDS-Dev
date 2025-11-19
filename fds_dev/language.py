import re

class LanguageDetector:
    """
    A simple language detector based on character sets.
    This is a basic implementation and not highly accurate. For production,
    a more robust library like 'langdetect' or 'fasttext' would be better.
    """
    # Unicode character ranges
    KOREAN_RE = re.compile(r"[\uac00-\ud7a3]")
    JAPANESE_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9faf]") # Hiragana, Katakana, Kanji
    CHINESE_RE = re.compile(r"[\u4e00-\u9fff]") # Common Chinese characters

    def detect(self, text: str, hint: str = 'en') -> str:
        """
        Detects the language of a given text.
        Returns a two-letter language code (e.g., 'ko', 'en').
        """
        text_sample = text[:200] # Analyze a sample for performance

        if self.KOREAN_RE.search(text_sample):
            return 'ko'
        
        # Japanese and Chinese share Kanji, so detection can be tricky.
        # A simple heuristic: if Hiragana/Katakana is present, it's likely Japanese.
        if self.JAPANESE_RE.search(text_sample) and not self.CHINESE_RE.search(text_sample.replace(' ', '')):
             return 'ja'

        if self.CHINESE_RE.search(text_sample):
            return 'zh'

        # Add more language detections here based on character sets or keywords
        # For example, for European languages:
        if ' un ' in text_sample and ' et ' in text_sample:
            return 'fr'
        if ' und ' in text_sample and ' das ' in text_sample:
            return 'de'
        if ' y ' in text_sample and ' el ' in text_sample:
            return 'es'

        # Default to the hint language, which is 'en' by default
        return hint

if __name__ == '__main__':
    detector = LanguageDetector()
    
    test_cases = {
        "ko": "이것은 한국어 문장입니다.",
        "ja": "これは日本語の文章です。",
        "zh": "这是一个中文句子。",
        "en": "This is an English sentence.",
        "fr": "C'est un chat et un chien.",
        "de": "Das ist eine Katze und das ist ein Hund."
    }

    for lang_code, text in test_cases.items():
        detected = detector.detect(text)
        print(f"Original ({lang_code}): '{text}' -> Detected: {detected}")

    # A case that might be ambiguous
    ambiguous_text = "東京" # Tokyo in Kanji (used in both Chinese and Japanese)
    print(f"Ambiguous: '{ambiguous_text}' -> Detected: {detector.detect(ambiguous_text)}")

