from urllib.request import urlopen
import json
import urllib
import logging
from django.apps import apps
import os



tool = "gene-protein-tool"
email = "voldrani@gmail.com"
eutils_base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
logger = logging.getLogger(__name__)

# For automated test, using static json files for eutils responses
gpt_base_dir = apps.get_app_config('gpt').path
test_eutils_dir = os.path.join(gpt_base_dir, "test_eutils")
test_eutils = False 

def read_test_file(name):
    logger.info("Fake eutils call; getting data from " + name)
    with open (os.path.join(test_eutils_dir, name), "r") as test_file:
        return test_file.read()



def esearch(term, db='gene', retmax=None):
    url = (
        eutils_base + '/esearch.fcgi?tool=' + tool + '&email=' + email + '&retmode=json' +
        ("&retmax=" + str(retmax) if retmax else "") +
        '&db=' + db + '&term=' + urllib.parse.quote_plus(term)
    )

    if (test_eutils == True):
        resp_str = read_test_file("esearch_human.json")
    else:
        logger.info("EUtilities call '" + url + "'")
        resp_str = urlopen(url).readall().decode('utf-8')
    logger.debug("Response: '" + resp_str + "'")

    return json.loads(resp_str)['esearchresult']


def esummary(idlist, db='gene'):
    if (len(idlist) == 0): return None

    idlist_str = idlist if type(idlist[0]) is str else map(str, idlist)
    url = (
        eutils_base + '/esummary.fcgi?tool=' + tool + '&email=' + email + '&retmode=json' +
        '&db=' + db + '&id=' + ",".join(idlist_str)
    )

    if (test_eutils == True and db == "gene"):
        resp_str = read_test_file("esummary_genes.json")
    elif (test_eutils == True and db == "protein"):
        resp_str = read_test_file("esummary_proteins.json")
    else:
        logger.info("EUtilities call '" + url + "'")
        resp_str = urlopen(url).readall().decode('utf-8')
    logger.debug("Response: '" + resp_str + "'")

    return json.loads(resp_str)['result']

# FIXME: which linkname should we use? gene_protein, or gene_protein_refseq?
def elink(idlist, dbfrom='gene', db='protein', linkname='gene_protein'):
    if (len(idlist) == 0): return None

    idlist_str = idlist if type(idlist[0]) is str else map(str, idlist)
    url = (
        eutils_base + '/elink.fcgi?tool=' + tool + '&email=' + email + '&retmode=json' +
        '&cmd=neighbor' +
        '&dbfrom=' + dbfrom + '&db=' + db + '&linkname=' + linkname +
        '&' + '&'.join(map( (lambda x: 'id=' + x), idlist_str ))
    )

    if (test_eutils == True):
        resp_str = read_test_file("elink.json")
    else:
        logger.info("EUtilities call '" + url + "'")
        resp_str = urlopen(url).readall().decode('utf-8')
    logger.debug("Response: '" + resp_str + "'")

    return json.loads(resp_str)['linksets']






