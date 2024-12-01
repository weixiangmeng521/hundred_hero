

# 纠正识别错别字
from defined import CORRECTION_DICT


def correct_text_handler(text):
    for incorrect, correct in CORRECTION_DICT.items():
        text = text.replace(incorrect, correct)
    return text.replace(" ", "").replace("\n", "")
