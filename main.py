import requests
from bs4 import BeautifulSoup
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np


# Website's module
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

"""
1. Get background image from website -> save as ./DB
2. Generate word cloud image depending on background image
3. Show generated image on website
"""


class CreateWordCloud:
    def __init__(self, subject):
        self.url: str = f"https://www.google.com/search?q={subject}&sxsrf=AJOqlzUkhgd9OvxXyTuPekS_n_3HvHVO6A:1677636607928&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjmh8-w07n9AhUYslYBHS6cDv8Q_AUoBHoECAEQBg&biw=960&bih=936&dpr=1" # url
        self.database_path = "./DB"
        self.main()

    """__main__"""
    def main(self):
        self.website()
        print(self.scap())
        self.wordclouding(self.scap())

    """Get background image and submit result picture"""
    def website(self):
        app = Flask(__name__)

        @app.route("/", methods=["POST","GET"])
        def upload_file():
            if request.method == "POST":
                f = request.files["file"]
                f.filename = "background.png"
                f.save(f"{self.database_path}/{secure_filename(f.filename)}")
            return render_template("index.html")

        app.run(debug=True)

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
        outputString = " ".join(outputString.split())

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
        img = Image.open(f"{self.database_path}/background.jpg")
        img_array = np.array(img)
        c = Counter(words) # words to dictortionary
        wc = WordCloud(font_path='malgun', width=400, height=400, scale=2.0, max_font_size=250, mask=img_array)
        gen = wc.generate_from_frequencies(c)
        plt.figure()
        plt.imshow(gen)
        plt.show()
        wc.to_file(f"{self.database_path}/cloudword.png")




if __name__=="__main__":
    cwc = CreateWordCloud("chatgpt")
