from collections import Counter
import os
import threading
import traceback

__author__ = 'veren_000'

threadLimiter = threading.BoundedSemaphore(8)
lock = threading.RLock()

artists_with_terms_count = {}


class TermCounter(threading.Thread):
    @staticmethod
    def get_artists_with_terms_count():
        return artists_with_terms_count

    @staticmethod
    def count_documents_containing_term(term):
        count = 0
        for artist in artists_with_terms_count.keys():
            if term in artists_with_terms_count[artist] and artists_with_terms_count[artist][term] > 0:
                count += 1
        return count

    def __init__(self, artist, term_index, artists_with_terms):
        threading.Thread.__init__(self)
        self.artist = artist
        self.term_index = term_index
        self.artists_with_terms = artists_with_terms

    def run(self):
        '''
        counts how often each term appears in a document
        :return:
        '''
        threadLimiter.acquire()

        # use counter for better performance
        counter = Counter(self.artists_with_terms[self.artist])

        termCountDict = {}
        for term in self.term_index:
            if term not in termCountDict:
                termCountDict[term] = counter[term]

        lock.acquire()
        try:
            artists_with_terms_count[self.artist] = termCountDict
        except Exception as ex:
            traceback.print_exc()
        finally:
            lock.release()

        threadLimiter.release()
