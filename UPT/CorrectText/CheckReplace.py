import os


def check(word, vocab):
    return word in vocab


def execute_alterations():
    pass

def drop_letter(word, count=1):
    return [ word[:idx]+word[idx+count:] for idx in range(len(word)) ]

def swap_order(word, count=1):
    return [ ]

def swap_substr(word, count, idx):
    return word[:idx]+word[idx+count:idx-1:-1]+word[idx+count:]