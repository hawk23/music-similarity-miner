__author__ = 'peter'

import nltk
import re

# todo for every file found in folder .\data\results
    # open a file
    # path = r".\data\test.txt"
    # txtFile = open(path, 'r')

    # read a file
    # text = txtFile.read()

    # close file descriptor
    # txtFile.close()

# just for testing
text = "<html><body>TEST testing tests are, will Hello world...artist Nice!!</title><h1>new</h1></body></html>"

# remove html and xml tags
text = re.sub("<.*?>", " ", text)

# remove unnecessary characters
chars_to_remove = ['.', ',', ';', ':', '!', '?', '$', '%', '*', '#', '<', '>', '(', ')', '[', ']', '{', '}', '/', '\\']
chars_to_remove.extend(['\'', '"', '-', '_', '|', '&', '^'])

text = text.translate(None, ''.join(chars_to_remove))

# convert text to lower letters
text = text.lower()

# build bag of words
wordArray = text.split(" ")

# stopping
stopWords = ["I", "a", "about", "an", "are", "as", "at", "be", "by", "com", "de", "en", "for", "from", "how", "in"]
stopWords.extend(["is", "it", "la", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when", "where"])
stopWords.extend(["who", "will", "with", "und", "the", "www"])

i = 0
while i < len(wordArray):
    # remove empty words
    if wordArray[i] == "":
        wordArray.pop(i)
    # check for stop words
    else:
        j = 0
        removed = False
        while j < len(stopWords):
            if wordArray[i] == stopWords[j]:
                wordArray.pop(i)
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
stemTool = nltk.SnowballStemmer("english")

i = 0
while i < len(wordArray):
    wordArray[i] = str(stemTool.stem(wordArray[i]))
    i += 1

# print the result
print wordArray
