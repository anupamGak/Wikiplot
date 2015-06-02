def pager(frag = "", title = ""):
	codeopen = """<!DOCTYPE html>
			  <html>
				<head>
				<title>Plot of %s</title>
			  </head>
			  <body>""" % title

	codeclose = """</body>
			   </html>"""

	code = codeopen + frag + codeclose
	return code