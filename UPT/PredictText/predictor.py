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

def get_restarter(data):
    # pick a random word from bag of words and return it
    restarter = "owen"
    return restarter


def generate_suggestions(words, context):
    # set word to last element in words
    word = words[-1]
    prev_words = words[len(words)-5:len(words)-1]
    # 1. pull top 30 trigrams from data
    tgs = collect_trigrams(data)
    # 2. get top bigrams using word
    bgs = collect_bigrams(word)
    # 3. remove words in previous words list from lists
    remove_words(prev_words,bgs,tgs)
    # 4. create a list to populate with top 3 suggested words
    suggestion_list = {}
    # if word and word-1 are the first 2 entries in a trigram, that should be #1
    for trigram in tgs:
        if str(prev_words[-1] + " " + word).lower() == str(trigram[0][0] + " " + trigram[0][0]).lower():
            suggestion_list.append(trigram[0][2])
    # fill remaining entries with 2 most common bigrams
    n = len(suggestion_list)
    for i in range(0, 3-n,1):
        # if bgs[i] is of type [[word1,word2],freq], this gets word2
        suggestion_list.append(bgs[i][0][1])        
    # if there are still less than 3 elements in suggestion_list, fill it with random words
    while len(suggestion_list) < 3:
        suggestion_list.append(context)









