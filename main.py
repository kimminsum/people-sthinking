<<<<<<< HEAD
import requests
from bs4 import BeautifulSoup
import re
import nltk


class Scrapping(object):
    def __init__(self, url):
        self.url: str = url # url
        print(self.scap())

    """Scrapping Data -> String"""
    def scap(self) -> list[str]:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        # Parsing data, HTML5 -> String
        tag = soup.body
        text_list: list = []
        # Remove special characters and Deduplication
        text_list = self.noun_extraction(list(set([self.clean_text(string) for string in tag.strings])))

        return text_list

    """Remove special characters"""
    def clean_text(self, inputString) -> str:
        outputString = re.sub('[-=+,#/\?:»^.@*\"※~ㆍ!』‘|\(\©>)\[\]`\'…》\”\“\’·]', ' ', inputString)
        outputString = ' '.join(outputString.split())

        return outputString

    """Extract noun"""
    def noun_extraction(self, inputString):
        # function to test if something is a noun
        is_noun = lambda pos: pos[:2] == "NN"
        tokenized = nltk.word_tokenize(inputString)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 

        return nouns


if __name__=="__main__":
    subject = "chatgpt"
    sp = Scrapping(f"https://www.google.com/search?q={subject}&sxsrf=AJOqlzUkhgd9OvxXyTuPekS_n_3HvHVO6A:1677636607928&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjmh8-w07n9AhUYslYBHS6cDv8Q_AUoBHoECAEQBg&biw=960&bih=936&dpr=1")
=======
import bs4
import request
# import selenium
>>>>>>> bfeff4f1578d66bf4fd5ade7a7b73294531ed199
