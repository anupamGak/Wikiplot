import zipfile
import re

reAbbr = re.compile("(?<= )[A-Z]")

container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
     media-type="application/oebps-package+xml" />
  </rootfiles>
</container>"""

content_opf = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"unique-identifier="bookid" version="2.0">
  <metadata>
    <dc:title>Plot: %s</dc:title>
    <dc:creator>Anupam Krishna</dc:creator>
    <dc:identifier id="bookid">urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658</dc:identifier>
    <dc:language>en-US</dc:language>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="cover" href="title.html" media-type="application/xhtml+xml"/>
    <item id="content" href="content.html" media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="cover" linear="no"/>
    <itemref idref="content"/>
  </spine>
  <guide>
    <reference href="title.html" type="cover" title="Cover"/>
  </guide>
</package>"""

toc_ncx = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>Movie Plot</text>
  </docTitle>
  <navMap>
    <navPoint id="navpoint-1" playOrder="1">
      <navLabel>
        <text>Book cover</text>
      </navLabel>
      <content src="title.html"/>
    </navPoint>
    <navPoint id="navpoint-2" playOrder="2">
      <navLabel>
        <text>Content</text>
      </navLabel>
      <content src="content.html"/>
    </navPoint>
  </navMap>
</ncx>"""

title_html = """<!DOCTYPE html>
<html>
<head>
	<title>Title</title>
</head>
<body>
	<h1>%s</h1>
	<p>Anupam Krishna</p>
</body>
</html>"""

def printEpub(htmlcode="", title=""):
	ttlAbr = title[0] + "".join(re.findall(reAbbr, title))
	epub = zipfile.ZipFile('epubs/plot_%s.epub' % ttlAbr, 'w')
	epub.writestr("mimetype", "application/epub+zip")
	epub.writestr("OEBPS/content.html", htmlcode)
	epub.writestr("OEBPS/content.opf", content_opf % title)
	epub.writestr("META-INF/container.xml", container_xml)
	epub.writestr("OEBPS/toc.ncx", toc_ncx)
	epub.writestr("OEBPS/title.html", title_html % title)
