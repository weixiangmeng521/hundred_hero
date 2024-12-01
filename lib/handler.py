# OCR 结果修正字典
correction_dict = {
    '什': '值',  # 例如将识别成 "什" 的词汇替换为 "值"
}

# 纠正识别错别字
def correct_text_handler(text):
    for incorrect, correct in correction_dict.items():
        text = text.replace(incorrect, correct)
    return text.replace(" ", "").replace("\n", "")
