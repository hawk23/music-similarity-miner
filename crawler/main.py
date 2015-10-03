import spider
import argparse

__author__ = 'mario'

parser = argparse.ArgumentParser()
parser.add_argument("inputFile")
parser.add_argument("outputDir")
args = parser.parse_args()

artists_file = args.inputFile
artists = open (artists_file, "r")

for line in artists:
    query = line.rstrip()

    sp = spider.Spider()
    rs = sp.fetchLinks(query)

    print '---------------'
    print 'fetched %s links for %s' % (len(rs), query)
    print 'downloading ...'

    out_file = args.outputDir + "/" + line.rstrip()+ ".txt"
    sp.download(rs, out_file)

    print 'saved to ' + out_file
