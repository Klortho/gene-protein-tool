# Gene protein tool

## Models / database schema


## Views

* Search page - displays a lone search box, and some exlanatory text


## Logging

By default, the app writes a log messages both to the console, and to a
log file to the project base directory, named gpt.log.
If you set the GTP_LOG_FILE environment variable, you can put that anywhere you want.


## To do

* get the search page working:
    * ✓Invoke esearch
    * ✓Move esearch into it's own module
    * ✓url encode: 'Homo sapiens [ORGN] AND Y [CHR]'
    * ✓Invoke esummary for genes
* ✓Turn off redirect temporarily. Output text.
* ✓Add logging messages. How to view Django logs?

* Create Gene model objects from the json returned.
