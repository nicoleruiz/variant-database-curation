#!/usr/bin/env python3

import html5lib
import requests # For this task, it's easier to use requests instead of selenium
import re
from collections import OrderedDict

# This script scrapes data from PAHvdb.

# There are 2 cookies for the page. This one is the one that is required for the script to work.
cookies = {'BIOPKUCopyrightDisclaimer': '1'}

# This has to be a post request. Can't do requests.get(URL).
r = requests.post(
    'http://biopku.org/pah/search-results-browse.asp',
    data={'searchType': '2'}, # This represents clicking search and browse to get to the list of all variants in the database
    cookies=cookies
)
doc = html5lib.parse(
    r.text, #input HTML
    treebuilder='lxml', #enable xpath function
    namespaceHTMLElements=False #disable namespace prefixes
)
links = doc.xpath('.//div[@id="container-body-wide"]//td[position()=4]//a')
#links = ['result-details-pah.asp?ID=689', 'result-details-pah.asp?ID=623','result-details-pah.asp?ID=622'] #for testing purposes
#links = ['result-details-pah.asp?ID=692', 'result-details-pah.asp?ID=693', 'result-details-pah.asp?ID=694', 'result-details-pah.asp?ID=733']

# Used this to check my regex https://pythex.org/
link_match = re.compile("/centralstore/pah/[a-zA-Z\.\d_\-()+]*_PAH.htm[l]?")

for link in links:
    r = requests.get('http://biopku.org/pah/' + link.attrib['href'], cookies=cookies)
    #r = requests.get('http://biopku.org/pah/' + link, cookies=cookies)
    doc = html5lib.parse(r.text, treebuilder='lxml', namespaceHTMLElements=False)
    rows = doc.xpath('.//div[@id="right-body"]//td')
    #print rows #this is blank [] for empty pages
    if rows:
        for r in rows:
            print ''.join([t for t in r.itertext()]).encode('utf-8').strip()
        pathogenicity_report = doc.xpath('.//div[@id="right-body"]//table[2]//tr[21]//td//a')
        # Either there is a link or the pathogenicity_report list is empty
        if pathogenicity_report:
            for p in pathogenicity_report:
                m = link_match.search(p.attrib['onclick'])
                if m:
                    r_report = requests.get('http://www.biopku.org' + m.group(), cookies=cookies)
                    report = html5lib.parse(r_report.text, treebuilder='lxml', namespaceHTMLElements=False)
                    p_elements = report.xpath('//body//p[2]')
                    for p in p_elements:
                        pathogenicity = ''.join([e for e in p.itertext()])
                        print 'Pathogenicity' + '\n' + pathogenicity
                    hgvs_table = report.xpath('//table//tr//td//b')
                    hgvs_keys = ['HGVS_c', 'HGVS_g', 'HGVS_p']
                    hgvs_values = []
                    for h in hgvs_table:
                        for b in h.itertext():
                            hgvs_values.append(b)
                    hgvs = OrderedDict(zip(hgvs_keys, hgvs_values))
                    for k,v in hgvs.iteritems():
                        print k + '\n' + v
