# using ntlk.ngrams to get the top 30 trigrams from data


from typing import Counter
import nltk
# from .Context import data_manager

def collect_trigrams(data):
    # returns a list of 30 most common trigrams
    trigrams = Counter(zip(*[data[i:] for i in range(3)]))
    # getting thirty most common
    return trigrams.most_common(3)

def collect_bigrams(word):
    # returns a list of 5 most common bigrams with "word" as 1st word
    pass

def remove_words(list, bg, tg):
    # removes words in list from trigram lists
    # this seems inefficient
    for badword in list:
        for t_entry in tg:
            if badword in t_entry:
                t_entry.delete()
        for b_entry in bg:
            if badword in b_entry:
                b_entry.delete()







