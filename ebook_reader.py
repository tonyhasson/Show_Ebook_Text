

import ebooklib
from bs4 import BeautifulSoup as bs
from ebooklib import epub
import pygame,time

##class
class Book:
    def __init__(self,text,name):
        self.text=text
        self.i=0
        self.j=0
        self.name=name
        self.end=False
        self.count_sentence=0
        self.sentence=""

    def set_end(self):
        self.end=True

    ##create text on screen
    def Create_Text(self):

        ##create sentence every 20 words
        if self.count_sentence % 20 == 0:
            self.sentence = self.find_sentence()
        string = self.Create_word()
        if string != False:
            ##show word on screen
            text_word = font1.render(string, True, white, black)
            textRect = text_word.get_rect()
            textRect.center = (X // 2, Y // 2 - 300)
            display_surface.fill(black)
            display_surface.blit(text_word, textRect)

            ##show sentence on screen
            text_sentence = font2.render(self.sentence, True, white, black)
            textRect = text_sentence.get_rect()
            textRect.center = (0, Y // 2)
            self.blit_text(display_surface, self.sentence, textRect.center, font2, white)
            pygame.display.update()

    ##create word from text
    def Create_word(self):
        string = ""

        if self.i < len(self.text):

            while self.j < len(self.text[self.i]) and self.text[self.i][self.j] == ' ':
                self.j += 1

            while self.j < len(self.text[self.i]) and self.text[self.i][self.j] != ' ':
                string += self.text[self.i][self.j]
                self.j += 1

            if self.j == len(self.text[self.i]):
                self.j = 0
                self.i += 1
            self.count_sentence += 1
            return string
        else:

            self.set_end()
            return False

    ##create 20 word sentence from text
    def find_sentence(self):

        i = self.i
        j = self.j
        string = ""
        t = 0
        while t < 20:
            if i < len(self.text):

                while j < len(self.text[i]) and self.text[i][j] == ' ':
                    j += 1
                if t != 0:
                    string += ' '
                while j < len(self.text[i]) and self.text[i][j] != ' ':
                    string += self.text[i][j]
                    j += 1

                if j == len(self.text[i]):
                    j = 0
                    i += 1

            t += 1
        return string

    ##show sentence text on screen(adds rows to the sentence)
    def blit_text(self,surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        position = 0
        for line in words:
            for word in line:

                if (self.count_sentence - 1) % 20 == position:
                    word_surface = font.render(word, 0, red)
                else:
                    word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
                position += 1
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    ##print the book
    def print_book(self):

        while self.end == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.Create_Text()

            time.sleep(0.6)


##list full of words to not include in the text

blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script',   ]

##functions for getting text from Ebook
def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

def chap2text(chap):
    output = ''
    soup = bs(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    rez = []
    for x in ttext:
        rez.append(x.replace("\n", ''))
    tmp=[]
    for x in rez:
        tmp.append(x.replace(u'\xa0', ''))
    return tmp

##text from Ebook
text=epub2text(r'C:\Users\tonyh\Downloads\harry-potter-book-1 (1).epub')


##creating the screen and sizes
X = 1000
Y = 800
pygame.init()
display_surface = pygame.display.set_mode((X, Y))

##creating title
pygame.display.set_caption("Ebook Reader")

##defining fonts and colors
font1 = pygame.font.Font('freesansbold.ttf', 76)
font2=pygame.font.Font('freesansbold.ttf', 60)
black=(0,0,0)
red=(220,0,0)
green = (0, 255, 0)
blue=(0,0,180)
white = (255, 255, 255)
yellow=(255,255,0)




obj=Book(text,"harry potter")
obj.print_book()
