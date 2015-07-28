#!/usr/local/bin/python3

import jinja2
import cgi
import cgitb
cgitb.enable()

results = None

templateLoader = jinja2.FileSystemLoader( searchpath="." )
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('search.html')

print("Content-Type: text/html\n")
print(template.render(results = results))


