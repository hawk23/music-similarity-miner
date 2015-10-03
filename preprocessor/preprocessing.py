__author__ = 'peter'

import nltk
import re
import os


def pre_process(path):
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
    __chars_to_remove.extend(['/', '\\' '\'', '"', '-', '_', '|', '&', '^', '\n'])

    # remove unnecessary characters
    __text = __text.translate(None, ''.join(__chars_to_remove))

    # convert text to lower letters
    __text = __text.lower()

    # build bag of words
    __wordArray = __text.split(" ")

    # stopping
    __stopWords = ["I", "a", "about", "an", "are", "as", "at", "be", "by", "com", "de", "en", "for", "from", "how"]
    __stopWords.extend(["in", "is", "it", "la", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when"])
    __stopWords.extend(["where", "who", "will", "with", "und", "the", "www"])

    i = 0
    while i < len(__wordArray):
        # remove empty words
        if __wordArray[i] == "":
            __wordArray.pop(i)
        # check for stop words
        else:
            j = 0
            removed = False
            while j < len(__stopWords):
                if __wordArray[i] == __stopWords[j]:
                    __wordArray.pop(i)
                    removed = True
                    break
                else:
                    j += 1
                    continue
            if not removed:
                i += 1

    # stemming
    # to check for other possible language remove #
    # print(" ".join(SnowballStemmer.languages))
    __stemmer = nltk.SnowballStemmer("english")

    i = 0
    while i < len(__wordArray):
        __wordArray[i] = str(__stemmer.stem(__wordArray[i]))
        i += 1

    return __wordArray


def main():
    dirname = "../data/results/"

    for filename in os.listdir(dirname):
        # print the result
        print filename + ":"
        print pre_process(dirname + filename)

    return

# run pre processing for each file
main()
