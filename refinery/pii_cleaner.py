import re

class PiiSanitizer:
    EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_REGEX = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    IP_REGEX = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

    @classmethod
    def sanitize_text(cls, text):
        if not text: return ""
        cleaned = re.sub(cls.EMAIL_REGEX, "[ANON_ENTITY]", str(text))
        cleaned = re.sub(cls.PHONE_REGEX, "[ANON_CONTACT]", cleaned)
        cleaned = re.sub(cls.IP_REGEX, "[ANON_IP]", cleaned)
        return cleaned.strip()
