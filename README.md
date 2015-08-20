# Gene protein tool

To run this:

```
git clone https://github.com/Klortho/gene-protein-tool.git
cd gene-protein-tool
pyvenv env
source env/bin/activate
```

***FIXME: install dependencies? requirements.txt? ***

To run the service:

```
cd project
./manage.py runserver
```


## Walk-through

This section describes a step-by-step walkthrough of the app, to see its features.
This can also be used as a manual test procedure.

* Bring up the app at http://localhost:8000
* Enter "human" in the search box
* Verify that you get a set of results corresponding to some genes, and their
  associated proteins

## Models / database schema

Right now, this uses a SQLite database.  To connect directly to the
database:

```
cd project
sqlite3 db.sqlite3
```

Then, examine tables with, for example,

```
.tables  # list all the tables
select * from gpt_gene 
...
```

To get out of the SQLite interpreter:

```
.exit
```

If you ever want to start over completely, discarding all old migratons,
do the following:

```
rm db.sqlite3
rm gpt/migrations/00*
./manage.py makemigrations
./manage.py migrate
```

Then, you'll also have to create a superuser for this application:

```
./manage.py createsuperuser
```

I created user `admin`, password `admin`.


To start the application with a brand-new database:





### Request / data model interaction

One of the main goals of this project is to allow users to create a result
set "report", which they can then save and bookmark. I want the resultant
report to be a static thing that won't change (unless the user himself 
decides to change it). 

Because the data coming from E-Utilities is subject to change, this means
that I want to save the results into the database, in order to ensure that
the generated report isn't dependent on the vagaries of NCBI.

But that introduces a problem. I don't want to create new Gene and Protein
records every time a user enters a query, since, for example, they might
enter the same query many times, and this would cause massive redundancy in
the database.

Here's the current strategy.  Everything is fluid until a ResultSet, and it's 
associated Genes and Proteins, gets saved. At that point, an "archive" flag 
gets set to True, and the records (but not the annotations, if any) become
read-only.

Specific behavior:

* When we get a query that's the same as that for an existing ResultSet, that
  doesn't have archive=True, update it. Otherwise, create a new ResultSet.
* When an esearch results in a gene UID corresponding to a Gene that exists in 
  the DB, that doesn't have archive=True, then update it. Otherwise create a 
  new Gene record.
* When an elink results in a protein UID corresponding to a Protein that exists
  in the database, that doesn't have archive=True, then update it. Otherwise,
  create a new Protein record.
* When the user clicks "save" on a result set display, then set archive=True on
  that ResultSet and all its corresponding Gene and Protein records.



## Views


### save

This view responds to Ajax POST requests that result from the user clicking the
"Save" button on the result set page. That POST request includes just one 
request parameter, `resultset_id`, which is the primary key of the result set
in the datbase.

Testing this by examining the Ajax request in the Chrome developer toolbar.

When there is any problem, this view returns with an HTTP error status, which
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



## Development / debugging


### Django admin app

Connect to the django admin app at [http://localhost:8000/admin/]().


### Django shell

You can connect to the django console with:

```
cd project
./manage.py shell_plus
```

This uses `shell_plus`, which preloads the models, plus some eutils routines,
as specified by `SHELL_PLUS_PRE_IMPORTS` in settings.py.

### Inspecting the database

Connect to the SQLite database with, for example:

```
$ cd project
$ sqlite3 db.sqlite3 
sqlite> .tables
auth_group                  django_migrations         
...                         ...
sqlite> select * from gpt_resultset;
5|2015-08-17 02:18:53.453206|human|1
...
.quit
```

