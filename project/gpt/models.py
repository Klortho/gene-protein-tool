from django.db import models
from gpt.eutils import *
import pprint
import logging
from project.settings import GPT

logger = logging.getLogger(__name__)

class ResultSet(models.Model):
    last_updated = models.DateTimeField(auto_now = True)

    # Create a new ResultSet from an Entrez query string.
    # This does not save the ResultSet, or any of the resultant Gene or
    # Protein objects, into the database.
    @classmethod
    def create_from_query(cls, query):
        rs = cls()

        esearch_result = esearch(query, db='gene', retmax=GPT['max_genes'])
        # Attach the results to the instance, for debugging
        rs.esearch_result = esearch_result

        # Limit the total number of genes here, based on settings
        gene_id_list = esearch_result['idlist'][0:GPT['max_genes']]

        esummary_genes = esummary(gene_id_list, db='gene')
        rs.esummary_genes = esummary_genes  # for debugging
        model_genes = []
        for guid in esummary_genes['uids']:
            #logger.info(guid)
            es_gene = esummary_genes[guid]
            g = Gene(uid=int(guid),
                     name=es_gene['name'],
                     description=es_gene['description'],
                     summary=es_gene['summary'])
            logger.debug("Found " + str(g))
            model_genes.append(g)


        elink_result = elink(gene_id_list)
        rs.elink_result = elink_result    # for debugging
        protein_ids = []
        max_proteins = GPT['max_proteins']
        max_proteins_per_gene = GPT['max_proteins_per_gene']
        for linkset_gene in elink_result:
            gene_id = linkset_gene['ids'][0]
            # Limit the number of proteins per gene
            links = linkset_gene['linksetdbs'][0]['links'][0:max_proteins_per_gene]
            # Limit the total number of proteins
            pb = max_proteins - len(protein_ids)
            protein_ids.extend(links[0:pb])


        #logger.info('protein_ids: ' + ",".join(map(str, protein_ids)))
        esummary_proteins = esummary(protein_ids, db='protein')
        rs.esummary_proteins = esummary_proteins   # for debugging
        model_proteins = []
        for pid in esummary_proteins['uids']:
            es_protein = esummary_proteins[pid]
            p = Protein(uid=int(pid),
                        caption=es_protein['caption'],
                        title=es_protein['title'])
            logger.debug("Found " + str(p))
            model_proteins.append(p)


        # FIXME - for now, we're not redirecting
        # Redirect to the page that will show the result.
        #return HttpResponseRedirect(reverse('gpt:result', args=(rs_id,)))

        return rs



class Gene(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    summary = models.TextField()

    def __str__(self):
        return "gene " + str(self.uid) + ": '" + self.name + "'"

class Protein(models.Model):
    gene = models.ForeignKey(Gene)
    uid = models.IntegerField()
    caption = models.CharField(max_length = 30)
    title = models.CharField(max_length = 80)

    def __str__(self):
        return "protein " + str(self.uid) + ": " + self.caption + " - '" + self.title + "'"
