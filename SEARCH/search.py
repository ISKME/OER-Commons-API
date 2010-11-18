#!/usr/bin/python

# A demo / testing script that uses the search functionality of the 
# OER Commons API.

import urllib

def utf8(s):
    return unicode(s, "utf-8")

class Search(object):
    def __init__(self, item):
        #self.grade_level = utf8(item["grade_level"])
        self.title = utf8(item["title"])
        self.url = utf8(item["url"])
        self.id = item["id"]

def getsearch(batchsize,batchstart,searchlabel,searchvalue):
    #url = "http://del.icio.us/feeds/json/%s/?raw" % user
    #url = "http://del.icio.us/feeds/json/%s/?raw" % user
    url = "http://staging.oercommons.org/api/search?batch_size=%d&batch_start=%d&%s=%s" % (batchsize, batchstart, searchlabel, searchvalue)
    return map(Search, eval(urllib.urlopen(url).read()))

# getsearch must run in batches of 50, so:
batch_size = 50
batch_start = 0
batch_complete = 0
fullsearch = []

while not batch_complete: 
    print batch_start
    searchsession = getsearch(batch_size,batch_start,"f.search","gregtest")
    #searchsession = getsearch(batch_size,batch_start,"f.search","suburbs")
    fullsearch += searchsession
    #print searchsession.id, searchsession.title, searchsession.url
    #print searchsession.title, searchsession.url
    if len(searchsession) == 50:
        batch_start += 50
    else:
        batch_complete = 1

print len(fullsearch)

for searchitem in fullsearch:
    print searchitem.title, searchitem.url, searchitem.id
