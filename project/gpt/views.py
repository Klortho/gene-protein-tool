from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
import pprint
import logging

from .models import *
from gpt.eutils import *

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'gpt/home.html', using = 'jinja2')

def search(request):
    # Get Genes and Proteins, create a results set, and store it to
    # the database.  Result set will go into rs.

    esearch_result = esearch(request.POST['term'], db='gene')
    idlist = esearch_result['idlist']

    esummary_genes = esummary(idlist, db='gene')
    model_genes = []
    for guid in esummary_genes['uids']:
        #logger.info(guid)
        es_gene = esummary_genes[guid]
        g = Gene(uid=int(guid),
                 name=es_gene['name'],
                 description=es_gene['description'],
                 summary=es_gene['summary'])
        logger.info(g)
        model_genes.append(g)

    elink_result = elink(idlist)
    protein_ids = []
    for linkset_gene in elink_result:
        gene_id = linkset_gene['ids'][0]
        links = linkset_gene['linksetdbs'][0]['links']
        #logger.info('gene_id = ' + str(gene_id))
        #logger.info('  links: ' + ",".join(map(str, links)))
        protein_ids.extend(links)

    logger.info('protein_ids: ' + ",".join(map(str, protein_ids)))
    esummary_proteins = esummary(protein_ids, db='protein')



    # FIXME - for now, we're not redirecting
    # Redirect to the page that will show the result.
    #return HttpResponseRedirect(reverse('gpt:result', args=(rs_id,)))

    return HttpResponse(
        #"esummary_genes\n==============\n" +
        #pprint.pformat(esummary_genes) + "\n\n" +
        "elink_result\n============\n" +
        pprint.pformat(elink_result) + "\n\n",
        content_type="text/plain"
    );


class ResultView(generic.DetailView):
    model = ResultSet
    template_name = 'gpt/result.html'
