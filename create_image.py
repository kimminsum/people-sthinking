import requests
from bs4 import BeautifulSoup
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np


class Scrapping:
    def __init__(self, url):
        self.url: str = url # url
        print(self.scap())
        self.wordclouding(self.scap())

    """Scrapping Data -> String"""
    def scap(self) -> list[str]:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        # Parsing data, HTML5 -> String
        tag = soup.body
        text_list: list = []
        extracted_text_list: list = []
        # Remove special characters and Deduplication
        text_list = (list(set([self.clean_text(string) for string in tag.strings])))
        for text in text_list:
            extracted_text_list.extend(self.noun_extraction(text))
        return extracted_text_list

    """Remove special characters"""
    def clean_text(self, inputString) -> str:
        outputString = re.sub('[-=+,#/\?:»^.@*\"※~ㆍ!』‘|\(\©>)\[\]`\'…》\”\“\’·]', ' ', inputString)
        outputString = ' '.join(outputString.split())

        return outputString

    """Extract noun"""
    def noun_extraction(self, inputString):
        # function to test if something is a noun
        okt = Okt()
        nouns = okt.nouns(inputString)
        words = [n for n in nouns if len(n) > 1]

        return words

    """Make Word Clouding"""
    def wordclouding(self, words):
        img = Image.open('background.jpg')
        img_array = np.array(img)
        c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
        wc = WordCloud(font_path='malgun', width=400, height=400, scale=2.0, max_font_size=250, mask=img_array)
        gen = wc.generate_from_frequencies(c)
        plt.figure()
        plt.imshow(gen)
        plt.show()
        wc.to_file("cloudword.png")


if __name__=="__main__":
    subject = "chatgpt"
    sp = Scrapping(f"https://www.google.com/search?q={subject}&sxsrf=AJOqlzUkhgd9OvxXyTuPekS_n_3HvHVO6A:1677636607928&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjmh8-w07n9AhUYslYBHS6cDv8Q_AUoBHoECAEQBg&biw=960&bih=936&dpr=1")