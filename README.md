# Gene protein tool

This application is a web interface to the NCBI 
[gene](http://www.ncbi.nlm.nih.gov/gene) and 
[protein](http://www.ncbi.nlm.nih.gov/protein) databases, which allows
users to generate and save reports from search results sets.

The main problem that it attempts to address is the fact that in NCBI's
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



## Contents

* [Installation](#installation)
* [Walk-through](#walk-through)
* [Settings](#settings)
* [Models / database schema](#models--database-schema)
* [Request / data model interaction](#request--data-model-interaction)
* [Views](#views)
* [Logging](#logging)
* [Testing](#testing)
* [Django admin app](#django-admin-app)
* [Django shell](#django-shell)
* [Possible enhancements / future work](#possible-enhancments--future-work)
* [License](#license)


## Installation

To run this:

```
git clone https://github.com/Klortho/gene-protein-tool.git
cd gene-protein-tool
./get-libraries.sh     # Downloads some JS libraries
pyvenv env
source env/bin/activate

pip install -r requirements.txt

cd project
./manage.py migrate
./manage.py createsuperuser   # create user `admin`
./manage.py test
./manage.py runserver
```

Then, open your browser to [http://localhost:8000](http://localhost:8000).



## Walk-through

This section describes a step-by-step walkthrough of the app, to see its features.
This can also be used as a manual test procedure.


### Bring up the app

* Open [http://localhost:8000](http://localhost:8000) in your browser. 
  You'll see the home page.
* You won't be logged in yet, so you should see "Register" and
  "Login" links 

### Do a search

* Enter "human" in the search box, and click "Submit"
* After a short time, you should get a page that has a list of ten
  genes
* Each gene will have up to five proteins associated with it
* The links to each gene and protein header goes to the corresponding
  record in the NCBI databases
* Many of the other items in the results display are linked to the 
  NCBI database as well, including organisms, bioprojects, genome
  assemblies, chromosome sequence records, etc.
* Each gene has 0 - many location information records. These are displayed
  in a collapsible table (collapsed by default)

### Back to the home page

* Click the header at the top of the results set display. You'll go back to
  the home page.
* Now, you should see this query listed under "Search history". 
* The "Saved?" column is blank, because we haven't saved that query yet.
  Query results sets are subject to change until they get saved, at 
  which point they become frozen and immutable.
* Make a note of the "last updated" time


### Search history

* Click "human" in the search history list. You will get back to the query 
  results page.
* Note that we went directly to the results page -- the search term was
  not re-evaluated. 
* You could also copy-paste the URL, and bring it up in another browser,
  and get the same results -- it is not dependant on the user session. 
* Since the search was not re-evaluated, the result-set, gene, and
  protein data all came directly out of the database. There were no
  new calls to E-utilities.
* Go back to the home page, and verify that the "last update" time
  has not changed.


### Re-do the same search

* Enter the exact same thing, "human", in the search box, and click the 
  "submit" button again
* Now, the search is re-evaluated anew. The application
  refreshes the result set, gene and protein data, with new calls to 
  NCBI E-utilities. 
* This is one area where the app could be improved: it
  should only make new calls to E-utilities, for a given gene or
  protein record, after some reasonable expiration period, perhaps
  one week.
* Note that the "Save result set" button is greyed-out. This is because
  we are not logged in. You can only save results sets after logging in.
* Click the header again to go back to the home page
* Note that even though the search was re-evaluated, there is still
  only one saved search for "human"
* Verify that now, the "last update" time has changed.


### Create an account, "alice"

* Click "Register"
* In the registration form that appears, enter the username "alice",
  and use the same value for the password.
* This is a very rudimentary user authentication system, and
  there is no mechanism to reset or change your password, or verify email
  addresses, or anything like that.
* After registering, you'll be redirected to the home page. You should
  now see "Logout" and "alice" in the upper right.
* For testing, click the "Logout" link now. You should become logged out, 
  and go immediately back to the home screen. The saved search
  list changes depending on whether or not you are logged in.
* Log back in as "alice"

### Same search again, under user account

* Enter the exact same search, "human"
* You will get another results set page, that looks just like the earlier
  one.
* Under the hood, this creates a new ResultSet model
  object (a new record in the gpt_resultset table), but not new gene or
  protein records. Those data records are shared by all active (not
  saved) result sets that reference them.

### Modify the search

* Now, in the results set page, modify the search to "human AND y[Chromosome]"
* You'll get a different set of genes and proteins.
* Go back to the home page, and you should see this new query in the list
* Click on the link, to go back to the results set page


### Saving a result set

* Click "Save result set". The button label should change to "Saved", and the
  button should become greyed out.
* This causes the database to set an "archived" flag on the result set, gene,
  and protein records. From now on, none of those database records will ever
  change.
* Because of this, a researcher could bookmark this URL, and cite it in his
  paper, and be sure that (assuming the web site were still around) it would
  be a permanent snapshot of the results at that instant in time.


### Saved result set behavior

* Click the header link to go back to the home page. Now, in the results
  list, you should see a check-mark in the "Saved?" column.
* Click the link for that query to go back to the results page. Make a note of
  the URL -- the number in the last path segment is the result set ID.
  Then click the "Submit" button next to the query.
* Unlike before, where running the same query updated the results, now,
  this will create a new result-set record, and new, mutable copies of each
  gene and protein record in the database.
* The result set ID in the URL should have changed.
* Go back to the home page, and now, in the search list, you should see two
  queries for "human AND y[Chromosome]"; one saved and one not.
* Copy this URL, and save it somewhere.

### Register a new user account, "bob"

* Click the "logout" link. You'll go back to the home page, with the search
  result for the "anonymous user".
* Click "register", and create a new account, with username "bob". 
  Now, in the home page, you should not see any search results.
* This feature allows each user to keep his/her own lists of search results.
  If they wanted to, they could even create project-specific user accounts,
  to get lists of search results specific to a given project. Of course,
  a more sophisticated approach, and one of the "future work" itesm, would
  be to allow for collections within user accounts.

### Edge cases

* Search for "fleegle". Verify that you get a page that says "No genes found".



## Settings

The application currently limits the number of genes returned in one result
set to 10, and the number of proteins per gene to 5.  These can be changed
in the project/settings.py file, at the, under the "GPT" settings.


## Models / database schema

Here is an entity-relationship diagram illustrating this application's data
model. Arrows indicate one-to-many relationships with the arrowhead on the 
"many" side. In other words, every user can have many resultsets.  

![Data model ERD](https://raw.githubusercontent.com/Klortho/gene-protein-tool/master/gene-protein-tool-erd.png)


The table "resultset-genes" is constructed automatically by Django, since the
ResultSet model, in models.py, contains this many-to-many specifier:

```
genes = models.ManyToManyField(Gene)
```


### Inspecting the database

Currently, this uses the SQLite database that is configured automatically when you
start a new Django project.  To connect directly to the database:

```
cd project
sqlite3 db.sqlite3
```

Then, examine tables with, for example,

```
.tables     # list all the tables
select * from gpt_gene 
...
```

To get out of the SQLite interpreter:

```
.exit
```

Another way to inspect the contents of the database is through the
Django admin app (see below).


### Recreating the database from scratch

To start over completely with the database, discarding all old migrations,
do the following:

```
rm db.sqlite3
git rm gpt/migrations/00*
./manage.py makemigrations
git add gpt/migrations
./manage.py migrate
./manage.py createsuperuser    # re-create user `admin`

```

Since the migration files are in Git, you should remove the old ones, and add
the new one, into the git repository.



## Request / data model interaction

One of the goals of this project is to allow users to create a result
set "report", which they can then save and bookmark. I want the resultant
report to be static and immutable, unless the user himself 
decides to change it. 

Because the data coming from E-Utilities is subject to change, this means
that I want to save the results into the database, in order to ensure that
the generated report isn't dependent on the vagaries of NCBI.

But that introduces a problem. I don't want to create new Gene and Protein
records every time a user enters a query, since, for example, they might
enter the same query many times, and this would cause massive redundancy in
the database.

The strategy I settled on is to allow for everything to be fluid and changeable,
up until the user explictly saves the result set. At that point, the result set,
the genes, and the proteins, and their associated records, get "frozen", and will
no longer be updated. I use a boolean field, "archived" to indicate these records.

The specific behavior is:

* When the app gets a query that's the same as that for an existing ResultSet,
  that doesn't have archived=True, and that was from the same user, then that
  ResultSet is updated. Otherwise, a new ResultSet is created.
* Each ResultSet has and "last_updated" field, that corresponds to the last time
  this query was run against E-Utilities, for that user.
* When an esearch results in a gene UID corresponding to a Gene that exists in 
  the DB, that doesn't have archived=True, then it is updated. Otherwise,
  a new Gene record is created.
* When an elink results in a protein UID corresponding to a Protein that exists
  in the database, that doesn't have archive=True, then update it. Otherwise,
  create a new Protein record.
* Note that Gene and Protein records, unlike ResultSet records, are not tied
  to an individual user. That means that a given ResultSet might link to Gene
  or Protein records that have been updated later than the ResultSet's
  last_updated time. I think this is a reasonable compromise.
* When the user clicks "save" on a result set display, then the archived field
  is set to True for that ResultSet and *all its corresponding Gene and Protein 
  records*. That means that these Gene and Protein records are no longer 
  available to participate in any new queries.



## Views

This application is configured to use Jinja2 templates for most of the
views.  The exceptions are the views related to user-authentication. Since
they were done at the last minute, and I couldn't figure out how to configure
the built-in user-authentication module to use Jinja2 templates.

URLs that this app handles are defined in:

* project/urls.py - this is the top-level, and includes:
    * /admin/* - the Django admin app's URLs; see below for more info.
    * /login/ - the [login view](#login-view); this is defined in the Django 
      user-authentication module
    * /register/ - the [register view](#register-view); a custom user-authentication URLs
    * /do_register/ - the [do_register view](#do_register); 
      which is the form handler for the /register/ form.
    * gpt/urls.py - defines GPT-specific URLs:
        * / - the [home view](#home-view)
        * /search/ - the [search view](#search-view)
        * /results/{id}/ - the [results view](#results-view)
        * /save/ - the [save view](#save-view)

### login view

This uses the project-level template file templates/registration/login.html.
This was adapted from an example in the Django documentation.

This one URL/view/template handles both presenting the form, and handling
the form data once it is filled in and POSTed back.

### register view

This view is defined in project/views.py, and uses the template file
templates/registration/register.html. It presents a simple form to the
user, and POSTs to the do_register view.

Note that unlike the *login* view, the *register* view doesn't come with the 
django.contrib.auth, so I made my own.


### do_register view

This view is defined in project/views.py, and handles the incoming form
data.  It does some validation on it, and if there is an error, it presents
a very rudimentary error page to the user.

If everything is successful, it creates the new user in the database, logs
in as that user, and redirects to the home view.

### home view

This is defined in gpt/views.py, and uses the template file
gpt/jinja2/gpt/home.html.

Note that that template, and the others in the GPT app, inherit from the
gpt/jinja2/gpt/base.html template, which defined the wrapper HTML, which
includes all the JS libraries and CSS files.

### search view

This is defined in gpt/views.py. It handles the search request, which is 
POST data from the search form. 
If successful, it creates a new ResultSet
and its associated data, and then redirects to the corresponding result view.

### results view

This view is defined in gpt/views.py, and uses the template
gpt/jinja2/gpt/result.html.

This takes the ID of the ResultSet in the final path segment of the URL.

It is quite a long template file, and includes a lot of conditionals, to
handle the variation in the data coming from E-utilities.

JavaScript and CSS are used extensively in this view to enhance the display
of the results. For example, a gene record might have many "location history"
records associated with it, which give the location of that gene in possible
many different assemblies. These records are displayed in a collapsible table,
that is collapsed by default. JavaScript is used to "uncollapse" the table,
when the user clicks on the control.


### save view

This view responds to Ajax POST requests that result from the user clicking the
"Save" button on the result set page. That POST request includes just one 
request parameter, `resultset_id`, which is the primary key of the result set
in the datbase.

If there is any problem, this view returns with an HTTP error status, which
then gets displayed by the JavaScript in an alert box.

When successful, this view returns status 200, and the JavaScript changes the
button label to "Saved", and disables it.


## Logging

By default, the app writes a log messages both to the console, and to a
log file to the project base directory, named gpt.log.
If you set the GTP_LOG_FILE environment variable, you can put that anywhere you want.

The logging is configured in the `LOGGING` section of settings.py. By default,
the log level both for the console and the log file is `DEBUG`.


## Testing

To run tests:

```
./manage.py test
```

### Testing eutils

I've saved several eutils responses to static json files, in gpt/test_eutils.
If, in eutils.py, you set `test_json` to `True`, then, for certain queries,
these static JSON resources will be used for the response instead of real HTTP requests
to NCBI.  Don't do that.  This is only to be used by the automated tests.

The test responses are from here:

* [esearch_human.json](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?tool=gene-protein-tool&email=voldrani@gmail.com&retmode=json&retmax=10&db=gene&term=human)
* [esummary_genes.json](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?tool=gene-protein-tool&email=voldrani@gmail.com&retmode=json&db=gene&id=106099058,106099000,106098772,106098764,106098726,106098694,106098364,106098298,106098248,106098126)
* [elink.json](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?tool=gene-protein-tool&email=voldrani@gmail.com&retmode=json&cmd=neighbor&dbfrom=gene&db=protein&linkname=gene_protein&id=106099058&id=106099000&id=106098772&id=106098764&id=106098726&id=106098694&id=106098364&id=106098298&id=106098248&id=106098126)
* [esummary_proteins.json](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?tool=gene-protein-tool&email=voldrani@gmail.com&retmode=json&db=protein&id=908541558,908512451,908446945,908446940,908446936,908528114,908454923,908498535,908535323,908535320,908510771,908431187,908529763,908529760)


## Django admin app

Connect to the django admin app at [http://localhost:8000/admin/]().

If necessary, login as the user `admin`. From there, you can view and modify
the database records.


## Django shell

You can connect to the django console with:

```
cd project
./manage.py shell_plus
```

This uses `shell_plus`, which preloads the models, plus some eutils routines,
as specified by `SHELL_PLUS_PRE_IMPORTS` in settings.py.


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


## License

![WTFPL](https://github.com/Klortho/gene-protein-tool/raw/master/wtfpl-badge-1.png)

See LICENSE.txt.
