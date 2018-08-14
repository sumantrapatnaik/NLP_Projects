############################################################
# Author: Sumantra Patnaik
############################################################

# Include your imports here, if any are used.
import math

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    listOflist_tok_POS = []
    tok_pos_tup = ()
    with open(path) as fp:
        filecontent = fp.read().splitlines()
        for eachline in filecontent:
            list_tok_POS = []
            tok_pos = eachline.split()
            for each_tok_pos in tok_pos:
                tok_pos_tup = tuple(each_tok_pos.split("="))
                list_tok_POS.append(tok_pos_tup)
            listOflist_tok_POS.append(list_tok_POS)

    return listOflist_tok_POS

    pass

def get_max_of_previous(v,T,N):
    list_max = []
    for i in range(N):
        list_max.append(v[i][T-1])
    return max(list_max)

def get_index_of_previous_max(v,T,N):
    list_max = []
    for i in range(N):
        list_max.append(v[i][T-1])
    return list_max.index(max(list_max)) + 1

class Tagger(object):

    def __init__(self, sentences):

        self.tags_list = []
        self.tokens_list = []
        tag_count_dict = {}
        self.init_tag_prob_dict = {}
        self.trans_prob_dict = {}
        self.emmission_prob_dict = {}

        for i in range(len(sentences)):
            for j in range(len(sentences[i])):

                if sentences[i][j][0] not in self.tokens_list:
                    self.tokens_list.append(sentences[i][j][0])

                if sentences[i][j][1] not in self.tags_list:
                    self.tags_list.append(sentences[i][j][1])

                if sentences[i][j][1] not in tag_count_dict:
                    tag_count_dict[sentences[i][j][1]] = 0
                else:
                    tag_count_dict[sentences[i][j][1]] += 1



        #For Transition probability calculation
        for a in range(len(self.tags_list)):
            self.init_tag_prob_dict[self.tags_list[a]] = 0
            for b in range(len(self.tags_list)):
                self.trans_prob_dict[(self.tags_list[a],self.tags_list[b])] = 0

        #For Emmission probability calculation
        for a in range(len(self.tokens_list)):
            for b in range(len(self.tags_list)):
                self.emmission_prob_dict[(self.tokens_list[a],self.tags_list[b])] = 0

        for i in range(len(sentences)):
            for j in range(len(sentences[i])):
                if j == 0:
                   self.init_tag_prob_dict[sentences[i][j][1]] += 1

                if j > 0:
                    self.trans_prob_dict[(sentences[i][j][1],sentences[i][j-1][1])] += 1


                self.emmission_prob_dict[(sentences[i][j][0],sentences[i][j][1])] += 1


        for i in range(len(self.tags_list)):
            init_prob = self.init_tag_prob_dict[self.tags_list[i]]
            self.init_tag_prob_dict[self.tags_list[i]] = math.exp(math.log(init_prob if init_prob > 0 else 0.000000001) - math.log(len(sentences)))

        for i in range(len(self.tokens_list)):
            for j in range(len(self.tags_list)):
                emm_prob = self.emmission_prob_dict[(self.tokens_list[i],self.tags_list[j])]
                self.emmission_prob_dict[(self.tokens_list[i],self.tags_list[j])] = math.exp(math.log(emm_prob if emm_prob > 0 else 0.000000001) - math.log(tag_count_dict[self.tags_list[j]]))


        for i in range(len(self.tags_list)):
            for j in range(len(self.tags_list)):
                if j > 0:
                    trans_prob = self.trans_prob_dict[(self.tags_list[i],self.tags_list[j])]
                    self.trans_prob_dict[(self.tags_list[i],self.tags_list[j])] = math.exp(math.log(trans_prob if trans_prob > 0 else 0.000000001) - math.log(tag_count_dict[self.tags_list[j]]))


        pass

    def most_probable_tags(self, tokens):
        most_prob_tags = []

        for token in tokens:
            emmsn_probs_token = []
            for i in range(len(self.tags_list)):
                emmsn_probs_token.append(self.emmission_prob_dict[(token,self.tags_list[i])])

            most_prob_tags.append(self.tags_list[emmsn_probs_token.index(max(emmsn_probs_token))])
        return most_prob_tags
        pass

    def viterbi_tags(self, tokens):
        states = self.tags_list

        T = len(tokens)  #columns -- observations length
        N = len(states)  #rows - State Graph length

        v = [0] * N
        for i in range(N):
            v[i] = [0] * T

        backpointer_matrix = [0] * N
        for i in range(N):
            backpointer_matrix[i] = [0] * T

        for i in range(N):
            v[i][0] = self.init_tag_prob_dict[states[i]] * self.emmission_prob_dict[(tokens[0],states[i])]
            backpointer_matrix[i][0] = 0

        for j in range(1,T):
            for i in range(N):
                v[i][j] = get_max_of_previous(v,j,N) * self.trans_prob_dict[(states[i],states[get_index_of_previous_max(v,j,N)])] * self.emmission_prob_dict[(tokens[j],states[i])]
                backpointer_matrix[i][j] = get_index_of_previous_max(v,j,N)


        last_max_index = get_index_of_previous_max(v,T,N)

        viterbi_tagList = []

        for i in range(len(tokens)):
            if i <> len(tokens) - 1:
                viterbi_tagList.append(states[backpointer_matrix[0][i+1]-1])
            else:
                viterbi_tagList.append(states[last_max_index-1])

        return viterbi_tagList

        pass
