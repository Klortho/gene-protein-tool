from urllib.request import urlopen
import json
import urllib
import logging


tool = "gene-protein-tool"
email = "voldrani@gmail.com"
eutils_base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
logger = logging.getLogger(__name__)


# FIXME
# for development, set retmax=2. Need to set this to 10 or some other number, when done.
retmax = 2

def esearch(term, db='gene'):
    url = (
        eutils_base + '/esearch.fcgi?tool=' + tool + '&email=' + email + '&retmode=json' +
        "&retmax=" + str(retmax) +
        '&db=' + db + '&term=' + urllib.parse.quote_plus(term)
    )
    logger.info("EUtilities call '" + url + "'")
    resp_str = urlopen(url).readall().decode('utf-8')
    return json.loads(resp_str)['esearchresult']



def esummary(idlist, db='gene'):
    idlist_str = idlist if type(idlist[0]) is str else map(str, idlist)
    url = (
        eutils_base + '/esummary.fcgi?tool=' + tool + '&email=' + email + '&retmode=json' +
        '&db=' + db + '&id=' + ",".join(idlist_str)
    )
    logger.info("EUtilities call '" + url + "'")
    resp_str = urlopen(url).readall().decode('utf-8')
    return json.loads(resp_str)['result']

# FIXME: which linkname should we use? gene_protein, or gene_protein_refseq?
def elink(idlist, dbfrom='gene', db='protein', linkname='gene_protein'):
    idlist_str = idlist if type(idlist[0]) is str else map(str, idlist)
    url = (
        eutils_base + '/elink.fcgi?tool=' + tool + '&email=' + email + '&retmode=json' +
        '&cmd=neighbor' +
        '&dbfrom=' + dbfrom + '&db=' + db + '&linkname=' + linkname +
        '&' + '&'.join(map( (lambda x: 'id=' + x), idlist_str ))
    )
    logger.info("EUtilities call '" + url + "'")
    resp_str = urlopen(url).readall().decode('utf-8')
    return json.loads(resp_str)['linksets']






