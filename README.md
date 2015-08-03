# Gene protein tool

## Models / database schema


## Views

* Search page - displays a lone search box, and some exlanatory text


## Logging

By default, the app writes a log messages both to the console, and to a
log file to the project base directory, named gpt.log.
If you set the GTP_LOG_FILE environment variable, you can put that anywhere you want.


## Testing


### Testing eutils

I've saved several eutils responses to static json files, in gpt/test_eutils.
If, in eutils.py, you set `test_json` to `True`, then, for certain queries,
these static JSON resources will be used for the response instead of real HTTP requests
to NCBI.  Don't do that.  This is only to be used by the automated tests.

The test responses are from here:

* [esearch_human.json](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?tool=gene-protein-tool&email=voldrani@gmail.com&retmode=json&retmax=10&db=gene&term=human)
* [esummary_genes.json](http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?tool=gene-protein-tool&email=voldrani@gmail.com&retmode=json&db=gene&id=106099058,106099000,106098772,106098764,106098726,106098694,106098364,106098298,106098248,106098126)


## To do

* Refactor, and implement some tests
    * ✓Move the code I have now to a ResultSet constructor
    * ✓Need to actually construct all of the objects.
        * Construct the proteins
    * Use a setting switch, and static versions of eutils json responses, to
      define a set of tests that will run "standalone"
        * For testing, use query "human", max_genes = 10, max_proteins_per_gene = 3,
          max_proteins = 25.
        * ✓http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?tool=gene-protein-tool&email=voldrani@gmail.com&retmode=json&retmax=10&db=gene&term=human
            - ✓Saved in esearch_human.json,
              to where? Look at how log file dir is specified, and copy that.
            - ✓Implemented in esearch()
    * Write the tests

