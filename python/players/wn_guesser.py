from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import wordnet_ic
from operator import itemgetter
from players.guesser import guesser
from collections import Counter
import numpy as np
import random


class wn_guesser(guesser):

    def get_board(self, words):

        self.words = words
        return words


    def get_clue(self, clue, num):

        self.clue = clue
        print("The clue is:", clue, num, sep=" ")

        li = [clue, num]
        return li


    def word_synset(self,clue, board):

        brown_ic = wordnet_ic.ic('ic-brown.dat')
        wup_results = []
        pat_results = []
        lch_results = []
        res_results = []
        jcn_results = []
        lin_results = []
        count = 0

        for i in (board):
            for clue_list in wordnet.synsets(clue):

                per_clue = wup_clue = pat_clue = res_clue = jcn_clue = lin_clue = 0

                for board_list in wordnet.synsets(i):

                    try:
                        # only if the two compared words have the same part of speech
                        wup = clue_list.wup_similarity(board_list)
                        pat = clue_list.path_similarity(board_list)
                        lch = clue_list.lch_similarity(board_list)
                        res = clue_list.res_similarity(board_list, brown_ic)
                        jcn = clue_list.jcn_similarity(board_list, brown_ic)
                        lin = clue_list.lch_similarity(board_list, brown_ic)

                    except:
                        continue

                    # if lch is non-zero so are the other 3 algorithms (same part of speech was compared)
                    if lch:

                        lch_results.append(("lch: ", lch, count, clue_list, board_list, i))
                        res_results.append(("res: ", res, count, clue_list, board_list, i))
                        jcn_results.append(("jcn: ", jcn, count, clue_list, board_list, i))
                        lin_results.append(("lin: ", lin, count, clue_list, board_list, i))
                        count += 1

                        if lch > per_clue:
                            per_clue = lch

                        if res > res_clue:
                            res_clue = res

                        if jcn > jcn_clue:
                            jcn_clue = jcn

                        if lin > lin_clue:
                            lin_clue = lin

                    # wup and path_sim always compares regardless of Part of Speech to an extent
                    if wup:

                        wup_results.append(("wup: ", wup, count, clue_list, board_list, i))
                        pat_results.append(("pat: ", pat, count, clue_list, board_list, i))
                        count += 1

                        if wup > wup_clue:
                            wup_clue = wup

                        if pat > pat_clue:
                            pat_clue = pat      

                print("lch: ", i, per_clue)
                print("wup: ", i, wup_clue)
                print("res: ", i, res_clue)
                print("jcn: ", i, jcn_clue)
                print("lin: ", i, lin_clue)
                print("pat: ", i, pat_clue)
                print('-'*30)

        # if results list is empty
        if not lch_results:
            return []

        wup_results = list(reversed(sorted(wup_results, key=self.take_second)))
        pat_results = list(reversed(sorted(pat_results, key=self.take_second)))
        lch_results = list(reversed(sorted(lch_results, key=self.take_second)))
        res_results = list(reversed(sorted(res_results, key=self.take_second)))
        jcn_results = list(reversed(sorted(jcn_results, key=self.take_second)))
        lin_results = list(reversed(sorted(lin_results, key=self.take_second)))

        results = [wup_results, pat_results, res_results, lch_results, lin_results, jcn_results]
        return results


    def give_answer(self):

        sorted_results = self.word_synset(self.clue, self.words)
        
        # if non empty result list
        if(sorted_results):

            first_index_row = [i[0] for i in sorted_results]


            for i in first_index_row:
                print(i)

            # simple voting alg
            most_common_word = []
            for i in range(0,5):
                most_common_word.append(sorted_results[i][0][5])

            most_list = []

            for i, count in Counter(most_common_word).most_common():
                if count != Counter(most_common_word).most_common(2)[0][1]:
                    break

                most_list.append(i)

            answer_input = random.choice(most_list)

        # result list was empty
        else:
            answer_input = "no comparisons"

        print(answer_input)
        
        return answer_input


    def take_second(self,elem):
        return elem[1]




