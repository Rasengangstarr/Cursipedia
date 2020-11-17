import curses
from curses import textpad
import requests
from bs4 import BeautifulSoup
import re
import wikipedia
from pick import pick

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def getTextForPage(title):
    paragraphs = []
   
    p = wikipedia.page(title)
    content = p.content # Content of page.
    content = content.encode("ascii", "ignore")
    content = content.splitlines()
    return content

def fitTextToScreen(text, sw):
    lines = []
    for l in text:
        chunks = [l[i:i+sw] for i in range(0, len(l), sw)]
        for c in chunks:
            lines.append(c)
    return lines

def showPage(stdscr, pageName, sh, sw):
    curses.curs_set(0)
    stdscr.clear()
    box = [[3,3], [sh-3, sw-3]]
    
    try:
        contents = getTextForPage(pageName)
    except wikipedia.DisambiguationError as e:
        title = 'Disambiguation error returned, which of these do you care about?'
        option, index = pick(e.options, title)
        showPage(stdscr, option, sh, sw)
        stdscr.refresh()
        return ""


    if contents == "":
        return

    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    
    stdscr.addstr(2, sw//2-len(pageName)//2, pageName)
    lines = fitTextToScreen(contents, sw-7)

    for i in range(sh-7):
        stdscr.addstr(i+4, 4, lines[i])

    stdscr.refresh()


def main(stdscr):
    sh, sw = stdscr.getmaxyx()
    while 1:
        key = stdscr.getch()

        if key == ord('s'):
            stdscr.clear()
            inp = curses.newwin(8,55, 0,0)
            inp.addstr(1,1, "What would you like to learn about?:")
            sub = inp.subwin(3, 41, 2, 1)
            sub.border()
            sub2 = sub.subwin(1, 40, 3, 2)
            tb = curses.textpad.Textbox(sub2)
            inp.refresh()
            tb.edit()
            showPage(stdscr, tb.gather()[:-2].rstrip(), sh, sw)
            # box = [[sh//2-3,sw//2-20], [sh//2+3,sw//2+20]]
            # textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
            # stdscr.addstr(sh//2-2, sw//2-17, "What would like to learn about?")
            # key = stdscr.getch()

curses.wrapper(main)

#contents = getTextForPage("Python programming language")
#print contents
# lines = fitParagraphsToScreen(paragraphs, 5)

