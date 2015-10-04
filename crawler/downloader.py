import threading
import urllib

__author__ = 'mario'

threadLimiter = threading.BoundedSemaphore(30)

class DownloaderTask(threading.Thread):

    def __init__(self, urls, out_file):
        threading.Thread.__init__(self)
        self.urls = urls
        self.out_file = out_file

    def run(self):
        print "started thread for %s: %s" % (self.out_file, self.getName())
        threadLimiter.acquire()
        try:
            self.download(self.urls, self.out_file)
        finally:
            threadLimiter.release()

        print "finished thread for %s: %s" % (self.out_file, self.getName())

    '''
    Downloads all files given in 'urls' and concatenates them into one single output file.
    '''
    def download(self, urls, out_file):
        myfile = open(out_file, "w")

        for url in urls:
            try:
                response = urllib.urlopen(url)
                html = response.read()
                myfile.write(html)
            except:
                pass

        myfile.close()