#!/usr/bin/env python
# ! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys
from collections import Counter


## Nombres: Susana Hueso Devís
# He incorporado Tri

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################



def sort_index(d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
      
        self.r1 = re.compile('[.;?!]')
        # token alfanumérico
        # pasarlo a minúsculas más tarde?
        self.r2 = re.compile('\W+')

    def index_sentence(self, sentence, tri):
        #############
        # COMPLETAR #
        #############
       
        if sentence:
            tokenized_sent = self.r2.split(sentence)
            tokenized_sentence = ['$'] + tokenized_sent + ['$']
            for word in range(len(tokenized_sentence)):
                if word < len(tokenized_sentence) - 1:                  
                    dual = tokenized_sentence[word]
                    if self.index['bi'].get(dual) is None:
                        self.index['bi'][dual] = []
               
                    self.index['bi'][dual].append("  " + tokenized_sentence[word + 1])
                if tri:

                    if word < len(tokenized_sentence) - 2:
                        triple = (tokenized_sentence[word], tokenized_sentence[word + 1])
                        if self.index['tri'].get(triple) is None:
                            self.index['tri'][triple] = []              
                        self.index['tri'][triple].append(tokenized_sentence[word + 2])

    ########################
    def compute_index(self, filename, tri):
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        raw_sentence = ""
        #############
        # COMPLETAR #
        #############
        with open(filename) as fh:
            for line in fh.readlines():
                sentencess = []
                raw_sentence = line
                sentencess.extend(self.r1.split(raw_sentence))               
                r3 = re.compile('\r\n?|\n+')
                sentences= []              
                for another_sentencess in sentencess:
                    sentences.extend(r3.split(another_sentencess))
                for sentence in sentences:
                    self.index_sentence(sentence.lower(), tri)

     
        for element in self.index['bi']:
            self.index['bi'][element] = Counter(self.index['bi'][element])
     
        if tri:
            for element in self.index['tri']:
                self.index['tri'][element] = Counter(self.index['tri'][element])

        ##############
        sort_index(self.index['bi'])
        if tri:
            sort_index(self.index['tri'])

    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)

    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)

    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])),
                          file=fh)

    def generate_sentences(self, n=10,tri = False):
        #############
        # COMPLETAR #
        #############
        n_copy = n
        control = True
        next_words_ap = ''
        next_word_next = ''
        list_of_words = []
        word = '$'
        counter = 0
        print('##########################################')
        print('################ BI ########################')
        print('##########################################')

        while n > 0:
            word_all_content = self.index['bi'].get(word)
            word_list = list(word_all_content)[1:][0]
       
            word_aparitions = [aparitions for (aparitions,next_word) in word_list]
            word_next = [next_word for (aparitions, next_word) in word_list]
            
            if control:
                control = False
                next_words_ap = word_aparitions
                next_word_next =   word_next

            # strip elimina espacios antes y después de strings
            # [0] para quitrarle las claves
            word = random.choices(word_next, word_aparitions)[0].strip()
            #print(word)

           
            if word == '$' or counter == 25:
                counter = 0
                n -= 1
                word = '$'
                # quitamos corchetes
                print(' '.join(list_of_words))
                list_of_words = []              
                continue

            counter += 1
            list_of_words.append(word)

        if tri:
            print('##########################################')
            print('################ TRI #######################')
            print('##########################################')
            word = '$'
            word2 = random.choices(next_word_next , next_words_ap)[0].strip()
            list_of_words = [word2]
            counter = 1
            n = n_copy
            while n > 0:
                word_all_content = self.index['tri'].get((word, word2))
                word_list = list(word_all_content)[1:][0]
                word_aparitions = [aparitions for (aparitions,next_word) in word_list]
                word_next = [next_word for (aparitions, next_word) in word_list]
                word = word2
                word2 = random.choices(word_next, word_aparitions)[0].strip()
            
                if word2 == '$' or counter == 25:
                    counter = 1
                    n -= 1
                    word = '$'
                    word2 = random.choices(next_word_next , next_words_ap)[0].strip()
                 
                    print(' '.join(list_of_words))
                    list_of_words = [word2]
                
                    continue

                counter += 1
                list_of_words.append(word2)




if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")
