# import enchant
import re

def proofread(text):
    result = text.replace("AITA", "Am I the asshole")
    # english_dict = enchant.Dict("en_US")

    # # Split the text into words
    # words = result.split()

    # # Check each word and replace misspelled words
    # corrected_words = words

    # # for word in corrected_words:
    # #     if not english_dict.check(word):
            
    # for i in range(0, len(corrected_words)):
    #     if should_replace_word(corrected_words[i]) and not english_dict.check(corrected_words[i]):
    #         suggestions = english_dict.suggest(corrected_words[i])
    #         if len(suggestions) != 0:
    #             corrected_words[i] = english_dict.suggest(corrected_words[i])[0]
    #             print("corrected word: " + corrected_words[i])

    # print(corrected_words)
    # return " ".join(corrected_words)
    return result

# def should_replace_word(word):
#     if word.isupper() or re.search(r'\d+[fFmM]', word) or word.lower() == "asshole":
#         return False
#     return True