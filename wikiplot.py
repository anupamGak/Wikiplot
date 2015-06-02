from lxml import html
import requests

schpage = html.parse("http://www.wikipedia.org").getroot()

search = raw_input("Search :")

schpage.forms[0].fields['search'] = search

wiki = html.parse(html.submit_form(schpage.forms[0])).getroot()

renodes = wiki.xpath("//h2[span='Plot']/following-sibling::*")

htmlfrag = ""
for renode in renodes:
	if renode.tag != 'h2':
		htmlfrag += html.tostring(renode)
	else:
		break

print htmlfrag