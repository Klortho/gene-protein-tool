from django.db import models
from gpt.eutils import *
import pprint
import logging
from project.settings import GPT

logger = logging.getLogger(__name__)


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

class ResultSet(models.Model):
    last_updated = models.DateTimeField(auto_now = True)
    genes = models.ManyToManyField(Gene)

    # Create a new ResultSet from an Entrez query string.
    # This does not save the ResultSet, or any of the resultant Gene or
    # Protein objects, into the database.
    @classmethod
    def create_from_query(cls, query):
        rs = cls()
        max_genes = GPT['max_genes']
        max_proteins = GPT['max_proteins']
        max_proteins_per_gene = GPT['max_proteins_per_gene']

        # Do ESearch to get the list of genes
        # -----------------------------------

        # `max_genes`, and the others, are typically enforced many times each
        esearch_result = esearch(query, db='gene', retmax=max_genes)
        # Attach the results to the instance, for debugging
        rs.esearch_result = esearch_result

        # Limit the total number of genes
        # In general, we'll always convert UID values into ints as soon as possible,
        # and always deal with them as ints in the program (even though they often
        # appear as strings in the JSON).
        gids = list(map(int, esearch_result['idlist'][0:max_genes]))

        # Do ESummary, db=gene, to get info about these genes; create Gene objects
        # ------------------------------------------------------------------------

        esummary_genes = esummary(gids, db='gene')
        rs.esummary_genes = esummary_genes  # for debugging
        my_genes = rs.my_genes = []
        gid_to_gene = {}   # cross reference a gene's UID to the Gene object
        for gid in gids:
            # FIXME: deal with error, when gid isn't found in results
            esummary_gene = esummary_genes[str(gid)]
            # FIXME: deal with errors when expected keys are not found
            g = Gene(uid=gid,
                     name=esummary_gene['name'],
                     description=esummary_gene['description'],
                     summary=esummary_gene['summary'])
            logger.debug("Found " + str(g))
            my_genes.append(g)
            gid_to_gene[gid] = g

        # Do ELink to get all the proteins associated with each of these genes
        # --------------------------------------------------------------------

        elink_result = elink(gids, 
                             dbfrom='gene', 
                             db='protein', 
                             linkname='gene_protein')
        rs.elink_result = elink_result    # for debugging

        # The elink results come back grouped by gene. Iterate over each gene, and
        # aggregate all the protein ids into one list. Also create a dictionary
        # to cross-reference pid to the Gene object
        pids = []
        pid_to_gene = {}
        gene_num = 0
        for linkset_gene in elink_result:
            # Enforce max_genes here, too. This shouldn't be necessary, but doesn't hurt:
            if (gene_num >= max_genes): break

            # Get the gene id from the result, and look up the Gene object
            gid = linkset_gene['ids'][0]
            gene = gid_to_gene[gid]

            # Get protein ids as integers. Limit the number of proteins per gene
            gene_pids = list(map(int,
                linkset_gene['linksetdbs'][0]['links'][0:max_proteins_per_gene]
            ))
            for pid in gene_pids:
                pid_to_gene[pid] = gene

            # Limit the *total* number of proteins ("pb" = protein budget)
            pb = max_proteins - len(pids)
            pids.extend(gene_pids[0:pb])
            if (len(pids) >= max_proteins): break
            gene_num = gene_num + 1

        # Do ESummary, db=protein, to get info about these proteins; create objects
        # -------------------------------------------------------------------------

        #logger.info('pids: ' + ",".join(map(str, pids)))
        esummary_proteins = esummary(pids, db='protein')
        rs.esummary_proteins = esummary_proteins   # for debugging
        proteins = rs.proteins = []
        for pid in pids:
            esummary_protein = esummary_proteins[str(pid)]
            p = Protein(uid=pid,
                        caption=esummary_protein['caption'],
                        title=esummary_protein['title'])
            logger.debug("Found " + str(p))
            proteins.append(p)

        # Save everything into the database, now that we've parsed all the 
        # E-utilities responses, and created all the
        # objects, with no errors.
        rs.save()
        for g in my_genes:
            g.save()
            rs.genes.add(g)

        for p in proteins:
            p.gene = pid_to_gene[p.uid]
            p.save()



        # FIXME - for now, we're not redirecting
        # Redirect to the page that will show the result.
        #return HttpResponseRedirect(reverse('gpt:result', args=(rs_id,)))

        return rs

