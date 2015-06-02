from lxml import html
import requests
import re
from pager import pager

reAnchor = re.compile("<a.+?>")
reTable = re.compile("<table[\w\W]+<\/table>")

search = raw_input("Search :")

schpage = html.parse("http://www.wikipedia.org").getroot()

schpage.forms[0].fields['search'] = search

wiki = html.parse(html.submit_form(schpage.forms[0])).getroot()

#getting the movie title
ttlcode = wiki.xpath("//h1")[0]
soup = html.tostring(ttlcode)
title = ttlcode.xpath("i/text()")[0]

#Getting the plot paragraphs
renodes = wiki.xpath("//h2[span='Plot']/following-sibling::*")
for renode in renodes:
	if renode.tag != 'h2':
		soup += html.tostring(renode)
	else:
		break

htmlfrag = re.sub(reAnchor, "", soup)
htmlfrag = re.sub("</a>", "", htmlfrag)
htmlfrag = re.sub(reTable, "", htmlfrag)

ePage = pager(htmlfrag, title)

with open('plots/plot%s.htm' % title, 'w') as f:
	f.write(ePage)
print "Done!"