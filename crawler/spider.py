from bs4 import BeautifulSoup
import re
import mechanize
import cookielib

__author__ = 'mario'


class Spider(object):

    def fetchLinks(self, query):
        links = []
        # create a browser
        br = self.initBrowser()

        # fetch first page
        url = 'http://duckduckgo.com/html/?q=%s' % (query)

        try:
            response = br.open(url)
            links += self.parseLinks(response)

            # invoke form to fetch second page
            br.select_form(nr=2)
            response = br.submit()
            links += self.parseLinks(response)
        except Exception,e:
            print "[ERR] could not fetch url %s: %s" % (url, str(e))

        return links

    def parseLinks(self, response):
        links = []
        parsed = BeautifulSoup(response.read())

        for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
            links.append(i.a['href'])

        return links

    def initBrowser(self):
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        return br
