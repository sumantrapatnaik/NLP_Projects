############################################################
# Author : Sumantra Patnaik
############################################################

############################################################
# Imports
import email
import collections
import math
import os
############################################################

# Include your imports here, if any are used.
#from collections import Counter
#from itertools import chain
#from nltk.tokenize import sent_tokenize, word_tokenize
############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    fp_emailpath = open(email_path)
    message = email.message_from_file(fp_emailpath)
    mylist = []
    list1 = []
    for body_line in email.iterators.body_line_iterator(message):
        list1 = body_line.split()
        for element in list1:
            mylist.append(element)

    fp_emailpath.close
    return mylist
    pass

def log_probs(email_paths,smoothing):
    token_list = []
    vocab_list = []

    for email_path in email_paths:
        token_list = load_tokens(email_path)   #get the list of tokens in each email_path
        for eachitem in token_list:
            vocab_list.append(eachitem)


    count_dict = dict(collections.Counter(vocab_list))  #dictionary to store word counts

    loglikelihood_dict = {}
    vocab_count = len(count_dict)   #vocabulary of the given email_paths

    sum_of_token_counts = sum(count_dict.values())

    for key, value in count_dict.items():
        loglikelihood_dict[key] = math.log((count_dict[key] + smoothing)
        /(sum_of_token_counts + smoothing * (vocab_count + 1)))

    loglikelihood_dict['<UNK>'] = math.log(smoothing/(sum_of_token_counts + smoothing * (vocab_count + 1)))

    return loglikelihood_dict
    pass

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        ham_paths1 = os.listdir(ham_dir)
        spam_paths1 = os.listdir(spam_dir)
        ham_paths = [ham_dir + "/" + x for x in ham_paths1]
        spam_paths = [spam_dir + "/" + y for y in spam_paths1]

        self.ham_log_prob_dict = log_probs(ham_paths,smoothing)
        self.spam_log_prob_dict = log_probs(spam_paths,smoothing)

        all_paths = ham_paths + spam_paths
        self.all_log_prob_dict = log_probs(all_paths,smoothing)


        #Start - > For calculating class probabilities
        count_ham = len(ham_paths)
        count_spam = len(spam_paths)

        self.prob_spam_class = count_spam/(count_spam + count_ham)
        self.prob_ham_class = count_ham/(count_spam + count_ham)
        #End -> For calculating class probabilities

        pass

    def is_spam(self, email_path):
        email_token_list = load_tokens(email_path)
        unknown_spamword_prob = self.spam_log_prob_dict['<UNK>']
        unknown_hamword_prob = self.ham_log_prob_dict['<UNK>']

        #Start -> For Spam Class probability
        sum_spam = self.prob_spam_class
        for token in email_token_list:
            if (token in self.all_log_prob_dict) and (token in self.spam_log_prob_dict):
                sum_spam = sum_spam + self.spam_log_prob_dict[token]
            else:
                sum_spam = sum_spam + unknown_spamword_prob

        #Start -> For Ham Class probability
        sum_ham = self.prob_ham_class
        for token in email_token_list:
            if (token in self.all_log_prob_dict) and (token in self.ham_log_prob_dict):
                sum_ham = sum_ham + self.ham_log_prob_dict[token]
            else:
                sum_ham = sum_ham + unknown_hamword_prob


        if sum_spam > sum_ham:
            return True
        else:
            return False

        pass

    def most_indicative_spam(self, n):
        spam_indication_dict = {}
        top_spams_list = []

        for token in self.all_log_prob_dict:
            if (token in self.ham_log_prob_dict) and (token in self.spam_log_prob_dict) and (token <> '<UNK>'):
                spam_indication_dict[token] = self.spam_log_prob_dict[token] - self.all_log_prob_dict[token]

        t = sorted(spam_indication_dict.iteritems(), key=lambda z:z[1],reverse=True)[:n]
        for z in t:
            top_spams_list.append("{0}".format(*z))

        return top_spams_list
        pass

    def most_indicative_ham(self, n):
        ham_indication_dict = {}
        top_hams_list = []
        for token in self.all_log_prob_dict:
             if (token in self.ham_log_prob_dict) and (token in self.spam_log_prob_dict) and (token <> '<UNK>'):
                 ham_indication_dict[token] = self.ham_log_prob_dict[token] - self.all_log_prob_dict[token]

        t = sorted(ham_indication_dict.iteritems(), key=lambda z:z[1],reverse=True)[:n]
        for z in t:
            top_hams_list.append("{0}".format(*z))

        return top_hams_list
        pass

#Main execution section of the program
sf = SpamFilter("homework1_data/train/spam","homework1_data/train/ham",0.00001)

if sf.is_spam("homework1_data/train/spam/spam3"):
    print "Yes it is a Spam !"
else:
    print "No it is not a Spam !"

print sf.most_indicative_spam(20)
print sf.most_indicative_ham(20)
