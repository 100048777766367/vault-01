import re

class StackedSieveRefinery:
    EMAIL_RGX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_RGX = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'

    @classmethod
    def purify(cls, raw_stream):
        clean_triplets = {}
        for item, source in raw_stream:
            # 1. Màng cú pháp
            s, p, o = "", "", ""
            if isinstance(item, dict):
                s, p, o = str(item.get("subject", "")), str(item.get("predicate", "")), str(item.get("object", ""))
            elif isinstance(item, str) and "--[" in item:
                try:
                    left, right = item.split("]--->" if "]--->" in item else "]-->")
                    s, p = left.split("--[")
                    o = right
                except Exception: continue

            # 2. Màng Zero-PII
            s = re.sub(cls.EMAIL_RGX, "[ANON]", s)
            s = re.sub(cls.PHONE_RGX, "[ANON]", s)
            o = re.sub(cls.EMAIL_RGX, "[ANON]", o)
            o = re.sub(cls.PHONE_RGX, "[ANON]", o)

            # 3. Màng bản quyền văn bản dài
            if len(s) > 75 or len(o) > 75 or len(s) < 2 or len(o) < 2: continue

            s = re.sub(r'[^\w\s\-_]', '', s).strip().capitalize()
            p = re.sub(r'[^\w\s\-_]', '', p).strip().replace(" ", "_").lower()
            o = re.sub(r'[^\w\s\-_]', '', o).strip().capitalize()

            # 4 & 5. Màng Byzantine & Khử trùng lặp
            key = f"{s}_{p}_{o}"
            if key not in clean_triplets:
                clean_triplets[key] = {"subject": s, "predicate": p, "object": o, "confidence": 0.95, "source": source}
            else:
                clean_triplets[key]["confidence"] = min(0.99, round(clean_triplets[key]["confidence"] + 0.01, 4))

        return list(clean_triplets.values())
