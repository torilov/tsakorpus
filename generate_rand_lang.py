
'''
a script for generating a random language with changable characteristics

'''

import json
import math
import string


ALPHABET = 'qwertyuiopasdfghjklzxcvbnmąóяŋ'
PUNKT = string.punctuation
MEAN_WORD_LENGTH = 5
MEAN_SENT_LENGTH = 10
MAX_SENT_LENGTH = 40
LENGTH_OF_CORPUS =  15*10**5
N_0 = 20000 # a constant for zipf's low
with open('grammar_features.json') as f:
    GRAMMAR = json.load(f)


class WordForm():
    """docstring for WordForm"""
    def __init__(self, freq):
        self.freq = freq


class Lexeme():
    """docstring for Lexeme"""
    def __init__(self, pos):
        self.pos = pos
        

def generate_wordforms():
    '''returns a list of wordforms (instances) with freqs'''
    n = calc_num_of_words()
    wfms_with_freq = []
    first = calc_f_0(n)
    for i in range(n//2):
        freq = first//(i + 1)
        print('current_freq: ' + str(freq))
        wfms_with_freq.append(WordForm(freq))
    wfms_with_freq += [WordForm(1) for i in range(n - n//2)]
    print(sum([wf.freq for wf in wfms_with_freq]))
    return wfms_with_freq


def make_freqs():
    n = calc_num_of_words()
    f_0 = culc_f_0(n)
    pass


def calc_f_0(n):
    sum_of_row = 0
    i = n//2
    while i >= 1:
        sum_of_row += 1/i
        i -= 1
    return round((LENGTH_OF_CORPUS - n/2)/sum_of_row)


def calc_num_of_words():
    gamma = 0.577
    disc = 1/4 + 2 * LENGTH_OF_CORPUS * ((math.log(N_0) + gamma + 1)/ N_0)
    n = 2 * (1/2 + math.sqrt(disc)) * N_0/(math.log(N_0) + gamma + 1)
    return round(n)


def generate_sents():
    current_length = 0
    while current_length < LENGTH_OF_CORPUS:
        pass


# if __name__ == '__main__':
#     generate_corp()
    
generate_wordforms()
