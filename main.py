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
        self.database_path = "./static"
        self.main()


    """__main__"""
    def main(self):
        self.website()


    """Get background image and submit result picture"""
    def website(self):
        app = Flask(__name__)

        @app.route("/", methods=["POST","GET"])
        def upload_file():
            image_file_path = f"{self.database_path}/IMG/waiting_background.png"
            
            # Get background image from website
            if request.method == "POST":
                f = request.files["file"]
                
                # Change file name as background.png
                f.filename = "background.png"
                
                # Save background image in "./DB/background.png"
                f.save(f"{self.database_path}/resulted_image/{secure_filename(f.filename)}")
                
                # Generate wordcloud
                print(self.scap())
                self.wordcloud_generate(self.scap())
                image_file_path = f"{self.database_path}/resulted_image/output.png"

        
            return render_template("index.html", user_image = image_file_path) # rendering index.html

        app.run(debug=True)


    """Make Word Clouding"""
    def wordcloud_generate(self, words):
        img = Image.open(f"{self.database_path}/resulted_image/background.png")
        
        # Change image to numpy array format
        img_array = np.array(img)
        c = Counter(words) # Words to dictortionary
        
        # Generate word cloud
        wc = WordCloud(font_path='malgun', width=1000, height=1000, scale=2.0, max_font_size=250, mask=img_array)
        gen = wc.generate_from_frequencies(c)
        
        # Show the resulted image -> Test
        plt.figure()
        plt.imshow(gen)
        plt.show()
        
        # Save generated image to ./DB/cloudword.png
        wc.to_file(f"{self.database_path}/resulted_image/output.png")


    """
    Scrapping data by list[str] format
    private: clean_text, noun_extraction
    """
    def scap(self) -> list[str]:
        page = requests.get(self.url)
        
        # Get html format text
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Extract body tag
        tag = soup.body
        text_list: list = []
        extracted_text_list: list = []
        
        # Remove special characters and Deduplication
        text_list = (list(set([self.clean_text(string) for string in tag.strings])))
        for text in text_list:
            # Extract noun in text
            extracted_text_list.extend(self.noun_extraction(text))

        
        return extracted_text_list


    """Remove special characters"""
    def clean_text(self, inputString) -> str:
        # Remove special characters in inputString
        outputString = re.sub('[-=+,#/\?:»^.@*\"※~ㆍ!』‘|\(\©>)\[\]`\'…》\”\“\’·]', ' ', inputString)
        
        # Remove space " "
        outputString = " ".join(outputString.split())

        
        return outputString # Summit converted inputString


    """Extract noun"""
    def noun_extraction(self, inputString) -> list[str]:
        # Function to test if something is a noun
        okt = Okt()
        nouns = okt.nouns(inputString)
        words = [n for n in nouns if len(n) > 1]

        
        return words





if __name__=="__main__":
    cwc = CreateWordCloud("chatgpt")
