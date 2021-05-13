# using ntlk.ngrams to get the top 30 trigrams from data


from typing import Counter
import os
import nltk
from UPT import CorrectText
from ..Context import data_manager as dm
from ..Context import context as c
import random

def collect_trigrams(word,prev_word,context):
    # returns 5 most common trigrams with "word"
    _, freq = context[word].get_context()
    freq_sort = sorted(freq.keys())
    tgs = set()
    p_tgs = set()
    if len(freq_sort) > 4:
        for i in range(0,5):
            tgs.add(freq[freq_sort[i]].token)
        _, freq2 = context[prev_word].get_context()
        freq2_sort = sorted(freq2.keys())
        if len(freq2_sort) > 4:
            for j in range(0,5):
                p_tgs.add(freq2[freq2_sort[i]].token)
        
    ovr = p_tgs & tgs
    if ovr:
        return ovr
    return None

def collect_bigrams(word, context):
    # returns a list of 5 most common bigrams with "word"
    _, freq = context[word].get_context()
    freq_sort = sorted(freq.keys())
    bgs = []
    for i in range(0,5):
        bgs.append(freq[freq_sort[i]].token)
    return bgs

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

def get_restarter(known_words):
    # pick a random word from data and return it
    r = random.randrange(400000)
    return known_words[r]


def generate_suggestions(words, context, known_words):
    # set word to last element in words
    word = words[-1]
    prev_words = words[len(words)-5:len(words)-1]
    # 1. pull top 30 trigrams from data
    tgs = collect_trigrams(word,prev_words[-1],context)
    # 2. get top bigrams using word
    bgs = collect_bigrams(word,context)
    # 3. remove words in previous words list from lists
    remove_words(prev_words,bgs,tgs)
    # 4. create a list to populate with top 3 suggested words
    suggestion_list = []
    # if we have a trigram, that should be #1
    if tgs:
        for trigram in tgs:
            suggestion_list.append(trigram)
    # fill remaining entries with 2 most common bigrams
    n = len(suggestion_list)
    if bgs:
        for i in range(0, 3-n,1):
            suggestion_list.append(bgs[i])        
    # if there are still less than 3 elements in suggestion_list, fill it with random words
    while len(suggestion_list) < 3:
        suggestion_list.append(get_restarter(known_words))









