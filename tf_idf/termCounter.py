from collections import Counter
import os
import threading
import traceback

__author__ = 'veren_000'


threadLimiter = threading.BoundedSemaphore(20)
lock = threading.RLock()

artistsWithTermsCount = {}

class TermCounter(threading.Thread):

    @staticmethod
    def getArtistsWithTermsCount():
        return artistsWithTermsCount

    @staticmethod
    def countDocumentsContainingTerm(term):
        count = 0
        for artist in artistsWithTermsCount.keys():
            if term in artistsWithTermsCount[artist]:
                count += 1
        return count

    def __init__(self, artist, artistsWithTerms):
        threading.Thread.__init__(self)
        self.artist = artist
        self.artistsWithTerms = artistsWithTerms

    def run(self):
        '''
        counts how often each term appears in a document
        :return:
        '''
        threadLimiter.acquire()
        print "started counting for %s %s" % (self.artist, self.getName())

        # use counter for better performance
        counter = Counter(self.artistsWithTerms[self.artist])

        termCountDict = {}
        for term in self.artistsWithTerms[self.artist]:
            if term not in termCountDict:
                termCountDict[term] = counter[term]

        lock.acquire()
        try:
            artistsWithTermsCount[self.artist] = termCountDict
        except Exception as ex:
            traceback.print_exc()
        finally:
            lock.release()

        print "finished counting for %s %s" % (self.artist, self.getName())
        threadLimiter.release()


