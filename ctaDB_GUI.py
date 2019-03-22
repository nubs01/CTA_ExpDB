import toga
import pandas as pd
from toga.style.pack import *

def build(app):
    box = toga.Box()
    container = toga.ScrollContainer()
    content = toga.Box(style=Pack(direction=COLUMN))
    for a in range(0,10):
        content.add((toga.Button('Hi',style=Pack(width=200,height=20))))
    container.content=content
    box.content = container
    return box


def main():
    return toga.App('ctaDB','com.rnanu.ctaDB',startup=build)

if __name__ == '__main__':
    main().main_loop()
