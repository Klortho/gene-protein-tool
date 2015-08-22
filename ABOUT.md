This page describes the Gene protein tool: what the motivation for it was,
the design strategy, challenges, and possible future work.

----

## Motivation

The main problem that this tool attempts to address is the fact that in NCBI's
web interface to the gene database, there is no simple report that lists both
the genes that match a query, along with the proteins associated with those
genes. Typically, multiple queries would need to be made, along with a lot
of cut-and-pasting, in order to get the information in one document.

The origin of this idea is from the NCBI [webinar on the edirect 
utilities, part 4](https://www.youtube.com/watch?v=d6-2KqQ_2QM). 
NCBI provides fantastic displays for individual gene, and individual protein 
records, but it is difficult to get a display that provides information about 
a gene and all of its associated protein products, all on one page. 
In the linked video, a method is described to generate these kinds of reports 
using command line utilities. This project is a web interface to do this.

Another problem that this project attempts to address is that of "link rot".
The fact is that often, citations in journal articles, especially to things
found on the web, are ephemeral and subject to deletion, being moved, or having
their contents change. One service that attempts to address this problem is
the [Internet Archive](https://archive.org/) (the "Wayback Machine"). This
allows users to grab a snapshot of a web page, and provides a URL to that
static snapshot, that can then be used in citations.

This project attempts to illustrate the it is relatively easy to address
that problem at its source. Web services in the bioinformatics (and in any
science, in general) should allow for results to be captured and saved by
users in a static form, that they can then use in citations in their
articles.


## Overview of the service

So, the main product of this utility is a static, saved report that shows 
a snapshot of the genes and their related proteins, at the time that the 
report was generated. The user can save the report, at which point it will
be "archived" in the database, and assigned a unique key. Once archived,
the data is immutable, and will not be changed. At that point, the URL
can be used in a journal article, bookmarked, and/or sent to colleagues,
with the guarantee that later viewers will see the same report that was
originally generated.

This tool uses [NCBI E-Utilities](http://www.ncbi.nlm.nih.gov/books/NBK25501/)
to perform the searches and gather the data.

For example, if the user entered the following search:

    Homo sapiens [ORGN] AND Y [CHR]

Then the server-side program would relay this to E-Utilities, and perform the 
following queries. (Note that in these links, the ID lists are abbreviated to 
two IDs, for readability):

* ESearch: [http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=Homo%20sapiens%20%5BORGN%5D%20AND%20Y%20%5BCHR%5D&retmode=json](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=Homo%20sapiens%20%5BORGN%5D%20AND%20Y%20%5BCHR%5D&retmode=json)
* ESummary-gene: [http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?retmode=json&db=gene&id=6736,6473](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?retmode=json&db=gene&id=6736,6473)
* ELink: [http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?retmode=json&dbfrom=gene&id=6736&id=6473&db=protein&cmd=neighbor](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?retmode=json&dbfrom=gene&id=6736&id=6473&db=protein&cmd=neighbor)
* ESummary-protein: [http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?retmode=json&db=protein&id=556559970,556559965](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?retmode=json&db=protein&id=556559970,556559965)

The tool would then extract the important data for each gene, and their related proteins,
and store them into the SQL database, with a unique identifier for this query results
set. It then redirects to a URL that displays this same data, using the unique
identifier to extract the data from the database.

The tool implements a simple user account / authentication system, so that different 
users can each have their own list of saved searches.  Note that this user-account
system only controls which queries a user sees in his or her home page, not which
results set he or she can view.  All result sets pages are publicly visible,
provided you know the URL to use.


## Challenges faced

I decided to implement this utility in Django, rather than as a set of CGIs.
NCBI, where I work, has started moving towards Django, and therefore it makes
sense for me to learn it better. The learning curve was a bit steep, though, in
the scope of this short project.  I learned a good deal about how to do things
in Django, but I know that I only scratched the surface of this framework's
design patterns.  Learning to do things "the right way" in Django did slow me
down a bit, in that it often would have been quicker to just code something the
"quick and dirty way".

One hurdle that took longer than it should was figuring out how to integrate
Jinja2 with Django. Django comes bundled with it's own templating system, and
most of the documentation assumes that you'll be using that. The method for 
getting Jinja2 to work is not very well documented. Furthermore, all of the
template examples scattered throughout the Django documentation use the built-in
template-language syntax, and it wasn't always clear how to translate that to
get it to work in Jinja2.

I finally figured out how to write a module, in project/jinja2.py, that let me
add arbitrary python functions into the template context. That, then allowed me
to do introspection (introspect.getmembers) and pretty-printing data structures
(pprint.pformat), which helped me figure out what was going on during template
execution.

Implementing the "Save" button via Ajax was a bit of a challenge. One sticking
point was the CSRF (cross-site request forgery) system that Django uses. It
requires that a server-supplied hash key be echoed back with every POST request
that can potentially change the state of the database.  Normally, inside 
templates, a canned function can be used for this, that adds a hidden field
to an HTML form. To get it to work with Ajax, I finally figured out how to read
the CSRF token from the cookie value.


## Possible enhancements / future work

* Proteins should have a many-to-many relationship with Genes, rather than a
  one-to-many. That way, protein records could be shared among multiple genes,
  and that would mean less redundancy in the database.
* User's should have the ability to delete queries in their saved search list.
* Need to implement a garbage collector, that trashes old records that haven't
  been used for a long time.
* Use EFetch, instead of ESummary, to get much more/better data
* Add the ability for the user to add hand-written notes (annotations) that get
  added to the ResultSet, and/or individual genes or proteins.
* More testing, including both unit tests and functional tests with Selenium.
* Add a "save to figshare" feature, that allows users to upload their results
  in JSON format to fighare. At which point, it will have a DOI.
