__author__ = 'mario'

import urllib

def download(urls, out_file):
    myfile = open(out_file, "w")
    for url in urls:
        response = urllib.urlopen(url)
        html = response.read()
        myfile.write(html)
    myfile.close()
