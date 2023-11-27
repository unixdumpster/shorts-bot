# import enchant
import re

def proofread(text):
    result = text.replace("AITAH", "Am I the a whole").replace("AITA", "Am I the a whole").replace("TIFU", "Today I fudged up")
    return result