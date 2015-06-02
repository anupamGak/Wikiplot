from lxml import html
import requests
import re

reAnchor = re.compile("<a.+?>")
reTable = re.compile("<table[\w\W]+<\/table>")

search = raw_input("Search :")

schpage = html.parse("http://www.wikipedia.org").getroot()

schpage.forms[0].fields['search'] = search

wiki = html.parse(html.submit_form(schpage.forms[0])).getroot()

renodes = wiki.xpath("//h2[span='Plot']/following-sibling::*")

soup = ""
for renode in renodes:
	if renode.tag != 'h2':
		soup += html.tostring(renode)
	else:
		break

htmlfrag = re.sub(reAnchor, "", soup)
htmlfrag = re.sub("</a>", "", htmlfrag)
htmlfrag = re.sub(reTable, "", htmlfrag)
print htmlfrag