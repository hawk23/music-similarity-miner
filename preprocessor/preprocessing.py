import threading
import traceback

__author__ = 'peter'

import os

# Stop words used by Google
STOP_WORDS = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

threadLimiter = threading.BoundedSemaphore(8)
lock = threading.RLock()

artists_with_terms = {}


class Preprocessing(threading.Thread):
    @staticmethod
    def get_artists_with_terms():
        return artists_with_terms

    def __init__(self, path=''):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        splits = self.path.split(os.sep)
        artist = splits[len(splits) - 1][:-4]

        threadLimiter.acquire()

        wordArray = []
        try:
            wordArray = self.pre_process(self.path)
        except Exception as ex:
            print "stacktrace for artist " + artist
            traceback.print_exc()
        finally:
            threadLimiter.release()

        lock.acquire()
        try:
            artists_with_terms[artist] = wordArray
        except Exception as ex:
            traceback.print_exc()
        finally:
            lock.release()

    # A simple function to remove HTML tags from a string.
    # You can of course also use some fancy library. In particular, lxml (http://lxml.de/) seems a simple and good solution; also for getting rid of javascript.
    def remove_html_markup(self, s):
        tag = False
        quote = False
        out = ""
        # for all characters in string s
        for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c
        # return stripped string
        return out

    def pre_process(self, path):
        # open a file
        html_content = open(path, 'r').read()

        # Next we perform some text processing:
        # Strip content off HTML tags
        content_tags_removed = self.remove_html_markup(html_content)
        # Perform case-folding, i.e., convert to lower case
        content_casefolded = content_tags_removed.lower()
        # Tokenize stripped content at white space characters
        tokens = content_casefolded.split()
        # Remove all tokens containing non-alphanumeric characters; using a simple lambda function (i.e., anonymous function, can be used as parameter to other function)
        tokens_filtered = filter(lambda t: t.isalnum(), tokens)
        # Remove words in the stop word list
        tokens_filtered_stopped = filter(lambda t: t not in STOP_WORDS, tokens_filtered)
        # Store remaining tokens of current artist in dictionary for further processing
        ret = tokens_filtered_stopped
        print "File " + path + " --- total tokens: " + str(len(tokens)) + "; after filtering and stopping: " + str(len(tokens_filtered_stopped))

        return ret


