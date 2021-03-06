import spider
import argparse
import urllib
import downloader
import time

__author__ = 'mario'

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("inputFile")
parser.add_argument("outputDir")
args = parser.parse_args()

# define maximum number of threads
maxthreads = 10
threads = []

artists_file = args.inputFile
artists = open (artists_file, "r")

for line in artists:
    query = line.rstrip() +" music"
    query = urllib.quote_plus(query)

    sp = spider.Spider()
    rs = sp.fetchLinks(query)

    print 'fetched %s links for %s' % (len(rs), query)
    if len(rs) == 0:
        print '[WARN] no links fetched for %s' % (query)

    out_file_name = line.rstrip()
    # only allow alphanumerric chars and spaces in filenames
    out_file_name = "".join(x for x in out_file_name if x.isalnum() or x.isspace())
    out_file = args.outputDir + "/" + out_file_name + ".txt"

    # start thread to download sites for the current query
    thread = downloader.DownloaderTask(rs, out_file)
    threads.append(thread)
    thread.start()

    # wait for 2 sec to avoid being blocked by searchengine's bot detection
    time.sleep(2)

# wait for all threads to finish
for thread in threads:
    thread.join()

end_time = time.time()
elapsed = end_time - start_time
minutes = int(elapsed / 60)
seconds = int(elapsed % 60)

print "--- execution time: %sm%ss---" % (minutes, seconds)