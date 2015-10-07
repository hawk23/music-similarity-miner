from collections import Counter
import os
import threading
import traceback

__author__ = 'veren_000'

threadLimiter = threading.BoundedSemaphore(8)
lock = threading.RLock()

artistsWithTermsCount = {}


class TermCounter(threading.Thread):
    @staticmethod
    def get_artists_with_terms_count():
        return artistsWithTermsCount

    @staticmethod
    def count_documents_containing_term(term):
        count = 0
        for artist in artistsWithTermsCount.keys():
            if term in artistsWithTermsCount[artist] and artistsWithTermsCount[artist][term] > 0:
                count += 1
        return count

    def __init__(self, artist, termIndex, artistsWithTerms):
        threading.Thread.__init__(self)
        self.artist = artist
        self.termIndex = termIndex
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
        for term in self.termIndex:
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
