import threading
import traceback
from nltk.corpus import stopwords

__author__ = 'peter'

import nltk
import re
import os

threadLimiter = threading.BoundedSemaphore(30)
lock = threading.RLock()

artistsWithTerms = {}

class Preprocessing(threading.Thread):

    @staticmethod
    def getArtistsWithTerms():
        return artistsWithTerms

    # Removing stopwords. Takes list of words, outputs list of words.
    def remove_stopwords(self, l_words, lang='english'):
        l_stopwords = stopwords.words(lang)
        content = [w for w in l_words if w.lower() not in l_stopwords]
        return content

    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        splits = self.path.split(os.sep)
        artist = splits[len(splits)-1][:-4]

        threadLimiter.acquire()
        print "started thread for %s: %s" % (artist, self.getName())

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
            artistsWithTerms[artist] = wordArray
        except Exception as ex:
            traceback.print_exc()
        finally:
            lock.release()
        print "finished thread for %s: %s" % (artist, self.getName())

    def pre_process(self, path):
        # open a file
        __file = open(path, 'r')

        # read a file
        __text = __file.read()

        # close file descriptor
        __file.close()

        # remove html and xml tags
        __text = re.sub("<.*?>", " ", __text)

        # define set of unnecessary characters
        __chars_to_remove = ['.', ',', ';', ':', '!', '?', '$', '%', '*', '#', '<', '>', '(', ')', '[', ']', '{', '}']
        __chars_to_remove.extend(['/', '\\' '\'', '"', '-', '_', '|', '&', '^', '\n', '=', '~', '\t', '\r'])

        # remove unnecessary characters
        __text = __text.translate(None, ''.join(__chars_to_remove))

        # convert text to lower letters
        __text = __text.lower()

        # build bag of words
        __wordArray = __text.split(" ")

        # remove all empty strings
        __wordArray = filter(lambda a: a != '', __wordArray)

        # stopping
        __stopWords = ["I", "a", "about", "an", "are", "as", "at", "be", "by", "com", "de", "en", "for", "from", "how"]
        __stopWords.extend(["in", "is", "it", "la", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when"])
        __stopWords.extend(["where", "who", "will", "with", "und", "the", "www"])

        __wordArray = self.remove_stopwords(__wordArray, 'english')

        # stemming
        # to check for other possible language remove #
        # print(" ".join(SnowballStemmer.languages))
        __stemmer = nltk.SnowballStemmer("english")

        i = 0
        while i < len(__wordArray):
            try:
                __wordArray[i] = str(__stemmer.stem(__wordArray[i]))
                i += 1

            except UnicodeDecodeError:
                i += 1

        return __wordArray
