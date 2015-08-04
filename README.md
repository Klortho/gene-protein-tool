# Gene protein tool

## Models / database schema



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



## Logging

By default, the app writes a log messages both to the console, and to a
log file to the project base directory, named gpt.log.
If you set the GTP_LOG_FILE environment variable, you can put that anywhere you want.


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


## To do

* ✓Get rid of max_proteins.
* ✓Save the query into the ResultSet
* ✓Add archive field to all records

* ✓For proteins UIDs that we've seen before, update rather than create new. 
* ✓For genes
* ✓For results sets







