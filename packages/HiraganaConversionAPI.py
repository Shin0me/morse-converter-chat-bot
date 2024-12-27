#hiragana-katakana map was created by Chat-GPT
katakana_hiragana_map = {
    # Basic vowels
    "ア": "あ", "イ": "い", "ウ": "う", "エ": "え", "オ": "お",
    # K-row
    "カ": "か", "キ": "き", "ク": "く", "ケ": "け", "コ": "こ",
    # G-row (濁音)
    "ガ": "が", "ギ": "ぎ", "グ": "ぐ", "ゲ": "げ", "ゴ": "ご",
    # S-row
    "サ": "さ", "シ": "し", "ス": "す", "セ": "せ", "ソ": "そ",
    # Z-row (濁音)
    "ザ": "ざ", "ジ": "じ", "ズ": "ず", "ゼ": "ぜ", "ゾ": "ぞ",
    # T-row
    "タ": "た", "チ": "ち", "ツ": "つ", "テ": "て", "ト": "と",
    # D-row (濁音)
    "ダ": "だ", "ヂ": "ぢ", "ヅ": "づ", "デ": "で", "ド": "ど",
    # N-row
    "ナ": "な", "ニ": "に", "ヌ": "ぬ", "ネ": "ね", "ノ": "の",
    # H-row
    "ハ": "は", "ヒ": "ひ", "フ": "ふ", "ヘ": "へ", "ホ": "ほ",
    # B-row (濁音)
    "バ": "ば", "ビ": "び", "ブ": "ぶ", "ベ": "べ", "ボ": "ぼ",
    # P-row (半濁音)
    "パ": "ぱ", "ピ": "ぴ", "プ": "ぷ", "ペ": "ぺ", "ポ": "ぽ",
    # M-row
    "マ": "ま", "ミ": "み", "ム": "む", "メ": "め", "モ": "も",
    # Y-row
    "ヤ": "や", "ユ": "ゆ", "ヨ": "よ",
    # R-row
    "ラ": "ら", "リ": "り", "ル": "る", "レ": "れ", "ロ": "ろ",
    # W-row
    "ワ": "わ", "ヲ": "を", "ン": "ん",
    # Small letters
    "ャ": "ゃ", "ュ": "ゅ", "ョ": "ょ", "ッ": "っ", "ヮ": "ゎ"
}

hiragana_katakana_map = {
    # Basic vowels
    "あ": "ア", "い": "イ", "う": "ウ", "え": "エ", "お": "オ",
    # K-row
    "か": "カ", "き": "キ", "く": "ク", "け": "ケ", "こ": "コ",
    # G-row (濁音)
    "が": "ガ", "ぎ": "ギ", "ぐ": "グ", "げ": "ゲ", "ご": "ゴ",
    # S-row
    "さ": "サ", "し": "シ", "す": "ス", "せ": "セ", "そ": "ソ",
    # Z-row (濁音)
    "ざ": "ザ", "じ": "ジ", "ず": "ズ", "ぜ": "ゼ", "ぞ": "ゾ",
    # T-row
    "た": "タ", "ち": "チ", "つ": "ツ", "て": "テ", "と": "ト",
    # D-row (濁音)
    "だ": "ダ", "ぢ": "ヂ", "づ": "ヅ", "で": "デ", "ど": "ド",
    # N-row
    "な": "ナ", "に": "ニ", "ぬ": "ヌ", "ね": "ネ", "の": "ノ",
    # H-row
    "は": "ハ", "ひ": "ヒ", "ふ": "フ", "へ": "ヘ", "ほ": "ホ",
    # B-row (濁音)
    "ば": "バ", "び": "ビ", "ぶ": "ブ", "べ": "ベ", "ぼ": "ボ",
    # P-row (半濁音)
    "ぱ": "パ", "ぴ": "ピ", "ぷ": "プ", "ぺ": "ペ", "ぽ": "ポ",
    # M-row
    "ま": "マ", "み": "ミ", "む": "ム", "め": "メ", "も": "モ",
    # Y-row
    "や": "ヤ", "ゆ": "ユ", "よ": "ヨ",
    # R-row
    "ら": "ラ", "り": "リ", "る": "ル", "れ": "レ", "ろ": "ロ",
    # W-row
    "わ": "ワ", "を": "ヲ", "ん": "ン",
    # Small letters
    "ゃ": "ャ", "ゅ": "ュ", "ょ": "ョ", "っ": "ッ", "ゎ": "ヮ"
}


class HiraganaConversionAPI:
    def __init__(self):
        pass

    def katakana_hiragana_conversion(self,word:str,toHiragana:bool=True):
        if toHiragana:
            convertedWord:str = "".join([katakana_hiragana_map.get(letter,letter) for letter in word])
        else:
            convertedWord:str = "".join([hiragana_katakana_map.get(letter,letter) for letter in word])
        return convertedWord

if __name__ == "__main__":
    pass