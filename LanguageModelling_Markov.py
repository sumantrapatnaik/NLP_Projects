############################################################
# Author: Sumantra Patnaik
############################################################

############################################################
# Imports
############################################################
# Include your imports here, if any are used.
import string
import random
import math
############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    token_list = []
    token_list = text.split()
    final_token_list = []

    for item in token_list:

        spacedString = ""
        for char1 in item:
            if char1 not in string.punctuation:
                CharOP = char1
            else:
                CharOP = " %s " % char1

            spacedString += CharOP

        for eachitem in spacedString.split():
            final_token_list.append(eachitem)

    return final_token_list
    pass

def ngrams(n, tokens):
    start_tok = "<START>"
    end_tok = "<END>"
    new_token_list = []
    ngram_list = []

    for j in range(n-1):
        new_token_list.append(start_tok)

    new_token_list.extend(tokens)
    new_token_list.append(end_tok)

    context_tup = ()
    ngram_tup = ()

    for i in range(len(tokens)+1):
        context_tup = tuple(new_token_list[i:i+(n-1)])
        #token_tup = new_token_list[i+(n-1)]
        ngram_tup = (context_tup, new_token_list[i+(n-1)])
        #print ngram_tup

        ngram_list.append(ngram_tup)

    return ngram_list

    pass

def getStartingContext(n):
    start_tok = "<START>"

    new_token_list = []


    for j in range(n - 1):
        new_token_list.append(start_tok)
    return new_token_list
    pass

class NgramModel(object):

    def __init__(self, n):
        self.order = n
        self.total_grams_count = 0
        self.ngram_tup_list = []
        self.context_list = []

        pass

    def update(self, sentence):
        token_list = tokenize(sentence)
        n_grams_list = ngrams(self.order,token_list)

        contextList = [item[0] for item in n_grams_list]

        for item in contextList:
             self.context_list.append(item)

        self.ngram_tup_list.extend(n_grams_list)
        self.total_grams_count = len(self.ngram_tup_list)


        pass

    def prob(self, context, token):
        match_count = 0
        context_count = 0
        context_count = self.context_list.count(context)
        match_count = self.ngram_tup_list.count((context,token))

        prob_tok_context = float(match_count)/float(context_count)

        return prob_tok_context

        pass

    def random_token(self, context):
        sorted_token_list = []
        r = random.random()
        token_list = []

        ret_tok = ""
        for item in self.ngram_tup_list:
            if context == item[0]:
                token_list.append(item[1])
        sorted_token_list1 = sorted(token_list)


        #remove duplicates from list of tokens
        for item in sorted_token_list1:
            if item not in sorted_token_list:
                sorted_token_list.append(item)

        prob_dict = {}

        for eachtok in sorted_token_list:
            prob_dict[eachtok] = self.prob(context,eachtok)

        for i in range(len(sorted_token_list)):
            prob_sum_prior = 0
            prob_sum_post = 0
            for j in range(i):
                prob_sum_prior += prob_dict[sorted_token_list[j]]
            prob_sum_post = prob_sum_prior + prob_dict[sorted_token_list[i]]

            if (prob_sum_prior <= r) and (r < prob_sum_post):
                ret_tok = sorted_token_list[i]
                return ret_tok

        pass

    def random_text(self, token_count):
        rand_token_list = []
        strToReturn = ""
        start_tok = "<START>"

        new_token_list = []


        for j in range(self.order - 1):
            new_token_list.append(start_tok)


        context_tup = ()


        for i in range(token_count):
            context_tup = tuple(new_token_list[0:(self.order - 1)])
            new_token = self.random_token(context_tup)
            rand_token_list.append(new_token)

            if new_token == "<END>":
                new_token_list = getStartingContext(self.order)
            else:
                for k in range(self.order - 1):
                    if k < self.order - 2:
                        new_token_list[k] = new_token_list[k+1]
                    else:
                        new_token_list[k] = new_token

        for i in range(len(rand_token_list)):
            if i <> 0:
                CharOP = " %s" % rand_token_list[i]
                strToReturn += CharOP
            else:
                CharOP = "%s" % rand_token_list[i]
                strToReturn += CharOP

        return str(strToReturn)
        pass

    def perplexity(self, sentence):
        token_list = tokenize(sentence)
        ngram_tup_list = ngrams(self.order,token_list)


        total_grams_count = len(ngram_tup_list)
        perplexity_score = 0.0

        for i in range(total_grams_count):
            perplexity_score += math.log(float(1)/self.prob(ngram_tup_list[i][0],ngram_tup_list[i][1]))

        int_perplexity_score = math.exp(perplexity_score)
        final_perplexity_score = math.pow(int_perplexity_score,(float(1)/total_grams_count))
        return final_perplexity_score
        pass

def create_ngram_model(n, path):
    nGramModel = NgramModel(n)
    with open(path) as fp:
        filecontent = fp.read().splitlines()
        for eachline in filecontent:
            nGramModel.update(str(eachline))

    return nGramModel
    pass
