import os
from nltk.metrics import edit_distance
from ..Context import data_manager as dm
from ..Context import context as c

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def execute_alterations(word, count=1):
    options = []
    for permut in [drop_letter, swap_order, rev, replace_letter, add_letter]:
        options.extend(permut(word))
    return options

def add_letter(word, count=1):
    return [ word[:idx]+letter+word[idx:] for idx in range(len(word)) for letter in alphabet ]

def drop_letter(word, count=1):
    return [ word[:idx]+word[idx+count:] for idx in range(len(word)) ]

def swap_order(word, count=1):
    return [ word[idx:]+word[idx+1]+word[idx]+word[idx+1:]  for idx in range(len(word)-1) ]

def rev(word, count=1):
    return [ rev_substr(word, count, idx) for idx in range(len(word)) ]

def rev_substr(word, count, idx):
    return word[:idx]+word[idx+count:idx-1:-1]+word[idx+count:]

def replace_letter(word, count = 1):
    return [ word[:idx]+letter+word[idx+1:] for idx in range(len(word)) for letter in alphabet ]

def load_known_words():
    file_n = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../data/words.txt")
    word_s = set()
    with open(file_n,"r") as words:
        for word in words:
            word_s.add(word.strip("\n"))
    return word_s

def compute_distance(worda, wordb):
    return edit_distance(worda, wordb)

def use_context(total_words, known_words, tot_dict):
    potential_words = total_words & known_words
    max_f = 0
    max_w = ""
    if potential_words:
        for w in list(potential_words):
            if tot_dict[w][1] > max_f:
                max_f = tot_dict[w][1]
                max_w = w
        return max_w
    else:
        return None

def spell_check_driver(input_words, spell_dict, cm):
    # check if there are words before or back or both
    # if just one or the other reference that for context
    # if both, do intersection of options
    # and compute intersection of first deg sep and that
    # and then if thats empty do second degree
    # if we have neither, do dict of know words just by order of changing
    # if we have it in a context, then do by highest context value
    # spell_dict = load_known_words()
    # cm = dm.load_context(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../.."))

    l = len(input_words)
    output = []
    known_set = set(spell_dict)
    for ct,word in enumerate(input_words):
        if word in alphabet:
            output.append(word)
            continue
        if word not in spell_dict:
            first_deg_sep = execute_alterations(word)
            sec_deg_sep = execute_alterations(word,count=2)
            all_changes = set.union(set(first_deg_sep),set(sec_deg_sep))
            pre = ""
            pos = ""
            if ct-1 >= 0:
                pre = input_words[ct-1]
            if ct+1 < l:
                pos = input_words[ct+1]

            suggested = ""
            if pre and pos:
                ctx_pre_f = cm[pre].get_context()
                ctx_post_f = cm[pos].get_context()
                tot_dict = {**ctx_post_f,**ctx_pre_f}
                tot_ctx_wrds = set(ctx_pre_f.keys()) & set(ctx_post_f.keys())

                suggested = use_context(tot_ctx_wrds, all_changes, tot_dict)
            elif pre:
                ctx_pre_f = cm[pre].get_context()
                tot_ctx_wrds = set(ctx_pre_f.keys())
                suggested = use_context(tot_ctx_wrds, all_changes, ctx_pre_f)
            elif pos:
                ctx_post_f = cm[pos].get_context()
                tot_ctx_wrds = set(ctx_post_f.keys())
                suggested = use_context(tot_ctx_wrds, all_changes, ctx_post_f)

            if not suggested:
                first_deg_set = set(first_deg_sep)
                first_inter = known_set & first_deg_set
                if first_inter:
                    lst = list(first_inter)
                    lst_dict = {}
                    for test_word in lst:
                        dst = compute_distance(test_word, word)
                        lst_dict[dst] = test_word
                    suggested = lst_dict[sorted(lst_dict.keys())[0]]
                else:
                    sec_deg_set = set(sec_deg_sep)
                    second_inter = known_set & sec_deg_set
                    if not second_inter:
                        suggested = None
                        # we have no found words, this mispelled word is too messed up to be anything
                    lst = list(second_inter)
                    lst_dict = {}
                    for test_word in lst:
                        dst = compute_distance(test_word, word)
                        lst_dict[dst] = test_word
                    if lst_dict:
                        suggested = lst_dict[sorted(lst_dict.keys())[0]]
            if suggested:
                output.append(suggested)
            else:
                print("Unable to resolve improved spelling for word: %s" %word)
                output.append(word)
        else:
            output.append(word)
    return output
