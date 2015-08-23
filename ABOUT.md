# About the Gene-protein tool

This page describes the Gene protein tool: what the motivation for it was,
the design strategy, challenges, and possible future work.


## Contents

* [Motivation](#motivation)
* [Overview of the service](#overview-of-the-service)
* [Challenges faced](#challenges-faced)
* [Possible enhancements / future work](#possible-enhancements--future-work)


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
Often citations in journal articles, especially to internet sources,
are subject to deletion, being moved, or having
their contents change. An existing service that attempts to address this problem is
the [Internet Archive](https://archive.org/) (the "Wayback Machine"). This
allows users to grab a snapshot of a web page, and provides a URL to that
static snapshot, that can then be used in citations.

This project attempts to illustrate that it is relatively easy to address
that problem at its source. Web services in bioinformatics (and, in general,
any science) should allow for results to be captured and saved by
users in a static form, that they can then use in citations in their
articles.


## Overview of the service

The main product of this utility is a static, saved report that shows 
a snapshot of the genes and their related proteins, at the time that the 
report was generated. Each report has a unique URL, that can be saved and
shared with others. The user can save the report, at which point it will
be "archived" in the database. Once archived,
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
system only controls which queries a user sees in the list displayed on the home page, 
not which results set he or she can view.  All result sets pages are publicly visible
by anyone, given the URL.


## Challenges faced

I decided to implement this utility in Django, rather than as a set of CGIs.
The learning curve was a bit steep, in
the scope of this short project.  I learned a good deal about how to do things
in Django, but I know that I only scratched the surface of this framework's
rich design patterns.  Learning to do things "the right way" in Django did slow me
down sometimes. It often would have been quicker to code something the
"quick and dirty way".

One hurdle that took longer than it should was figuring out how to integrate
the [Jinja2 templating system](http://jinja.pocoo.org/) with Django. Django 
comes bundled with its own templating system, and
most of the Django documentation assumes that you are using that. The method for 
getting Jinja2 to work is not very well documented. Furthermore, it was often a
challenge to figure out how to translate various examples from the documentation
into the Jinja2 syntax.

I finally found a reference on how to write a Python module, which I put into
project/jinja2.py, that lets one add arbitrary Python functions into the 
template context. That allowed me
to do introspection (introspect.getmembers) and pretty-printing data structures
(pprint.pformat), which helped me figure out how to debug template
execution problems.

Implementing the "Save" button via Ajax was another challenge. It required 
understanding the CSRF (cross-site request forgery) system that Django uses. That
system uses a server-supplied hash key, that the client echos back with every POST 
request that can potentially change the state of the database.  Normally, inside 
templates, a canned function can be used to include the CSRF token, and add it
to a hidden field in an HTML form. To get it to work with Ajax, it was necessary
to use JavaScript to read the CSRF token from the cookie value directly.


## Possible enhancements / future work

Here is a list of things that could be improved with this service.

* User's should have the ability to delete queries in their saved search list.
* The tool needs a garbage collector, that discards old records that haven't
  been used for a long time.
* The tool should only make new calls to E-utilities, for a given gene or 
  protein record, after some reasonable expiration period -- perhaps one week.
  The NCBI data is subject to change, but not so often.
* There is a small bug in the way user accounts work:
  if one user is looking at a non-saved result set of another user, the "save 
  result set" button should only be greyed out. That is, only the user who
  "owns" a result set should be able to save it.
* Use EFetch, instead of ESummary, to get much more/better data about the Genes
  and Proteins.
* Add the ability for the user to add hand-written notes (annotations) that get
  added to the ResultSet, and/or individual genes or proteins.
* More testing, including both unit tests and functional tests with Selenium.
* Add a "save to Figshare" feature, that allows users to upload their results
  in JSON format to Fighare. At which point, it will have a DOI.
* Proteins should have a many-to-many relationship with Genes, rather than a
  one-to-many. That way, protein records could be shared among multiple genes,
  and that would mean less redundancy in the database. Whether or not this would
  really have an effect depends on how what percentage of proteins have links
  from multiple genes.
