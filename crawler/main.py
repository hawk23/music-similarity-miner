import spider
import argparse
import urllib

__author__ = 'mario'

parser = argparse.ArgumentParser()
parser.add_argument("inputFile")
parser.add_argument("outputDir")
args = parser.parse_args()

artists_file = args.inputFile
artists = open (artists_file, "r")

for line in artists:
    query = line.rstrip() +" music"
    query = urllib.quote_plus(query)

    sp = spider.Spider()
    rs = sp.fetchLinks(query)

    print '---------------'
    print 'fetched %s links for %s' % (len(rs), query)
    print 'downloading ...'

    out_file_name = line.rstrip()
    # only allow alphanumerric chars and spaces in filenames
    out_file_name = "".join(x for x in out_file_name if x.isalnum() or x.isspace())
    out_file = args.outputDir + "/" + out_file_name + ".txt"

    sp.download(rs, out_file)

    print 'saved to ' + out_file
