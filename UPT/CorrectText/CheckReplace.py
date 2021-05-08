import os
from ..Context import data_manager as dm
from ..Context import context as c

def execute_alterations(word, count=1):
    options = []
    for permut in [drop_letter, swap_order, rev]:
        options.extend(permut(word))
    return options

def drop_letter(word, count=1):
    return [ word[:idx]+word[idx+count:] for idx in range(len(word)) ]

def swap_order(word, count=1):
    return [word[idx+1]+word[idx]+word[idx+1:]  for idx in range(len(word)-1)]

def rev(word, count=1):
    return [rev_substr(word, count, idx) for idx in range(len(word))]

def rev_substr(word, count, idx):
    return word[:idx]+word[idx+count:idx-1:-1]+word[idx+count:]

def load_known_words():
    file_n = "../../data/words.txt"
    word_s = set()
    with open(file_n,"r") as words:
        for word in words:
            word_s.add(word)
    return word_s


def spell_check_driver(input_words):
    spell_dict = load_known_words()
    dm.load_context("../..")
    for word in input_words:
        if word not in spell_dict:
            first_deg_sep = execute_alterations(word)
            sec_deg_sep = execute_alterations(word,count=2)

