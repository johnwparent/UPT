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

def get_restarters(data):
    # pick 10 random words from bag of words and stick them in an array
    restarters = {}
    for i in range(0,10,1):
        restarters.append() #pick a random number and add bag of words entry to restarters
    return restarters



def generate_suggestions(word, prev_words):
    # calls other functions to return 3 selected words
    # 1. pull top 30 trigrams from data
    tgs = collect_trigrams(data)
    # 2. get top bigrams using word
    bgs = collect_bigrams(word)
    # 3. remove words in previous words list from lists
    remove_words(prev_words,bgs,tgs)
    # 4. create a list to populate with top 3 suggested words
        # if word and word-1 are the first 2 entries in a trigram, that should be #1
        # fill remaining entries with 2 most common bigrams
        # fill remaining spots with random words






