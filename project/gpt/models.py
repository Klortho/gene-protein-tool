from django.db import models
from gpt.eutils import *
import pprint
import logging
from project.settings import GPT
import dateutil.parser

logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


# Gene model

class Gene(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    chromosome = models.CharField(max_length = 10)
    geneticsource = models.CharField(max_length = 30)
    organism_name = models.CharField(max_length = 100)
    organism_commonname = models.CharField(max_length = 50)
    organism_taxid = models.IntegerField()
    summary = models.TextField()
    archived = models.BooleanField(default = False)

    def __str__(self):
        return "gene " + str(self.uid) + ": '" + self.name + "'"

class GenomicInfo(models.Model):
    gene = models.ForeignKey(Gene)
    chrloc = models.CharField(max_length = 20)
    chraccver = models.CharField(max_length = 20)
    chrstart = models.IntegerField()
    chrstop = models.IntegerField()
    exoncount = models.IntegerField()

class LocationHist(models.Model):
    gene = models.ForeignKey(Gene)
    annotationrelease = models.CharField(max_length = 20)
    assemblyaccver = models.CharField(max_length = 30)
    chraccver = models.CharField(max_length = 20)
    chrstart = models.IntegerField()
    chrstop = models.IntegerField()


# Protein model

class Protein(models.Model):
    gene = models.ForeignKey(Gene)
    uid = models.IntegerField()
    caption = models.CharField(max_length = 30)
    title = models.CharField(max_length = 80)
    extra = models.CharField(max_length = 80)
    gi = models.IntegerField(null = True)
    createdate = models.DateField(null = True)
    updatedate = models.DateField(null = True)
    taxid = models.IntegerField(null = True)
    slen = models.IntegerField(null = True)
    projectid = models.CharField(max_length = 20)
    genome = models.CharField(max_length = 20)
    organism = models.CharField(max_length = 50)


    archived = models.BooleanField(default = False)

    def __str__(self):
        return "protein " + str(self.uid) + ": " + self.caption + " - '" + self.title + "'"


# ResultSet model

class ResultSet(models.Model):
    last_updated = models.DateTimeField(auto_now = True)
    genes = models.ManyToManyField(Gene)
    query = models.CharField(max_length = 200)
    archived = models.BooleanField(default = False)

    # Create a new ResultSet from an Entrez query string.
    # This does not save the ResultSet, or any of the resultant Gene or
    # Protein objects, into the database.
    @classmethod
    def create_from_query(cls, query):
        try:
            rs = cls.objects.get(query = query, archived = False)
            debug_msg = "Updating "
        except cls.DoesNotExist:
            rs = cls(query=query)
            debug_msg = "Creating new "

        #rs = cls(query = query)
        max_genes = GPT['max_genes']
        max_proteins_per_gene = GPT['max_proteins_per_gene']

        # Do ESearch to get the list of genes
        # -----------------------------------

        # `max_genes`, and the others, are typically enforced many times each
        esearch_result = esearch(query, db = 'gene', retmax = max_genes)
        # Attach the results to the instance, for debugging
        rs.esearch_result = esearch_result

        # Limit the total number of genes
        # In general, we'll always convert UID values into ints as soon as possible,
        # and always deal with them as ints in the program (even though they often
        # appear as strings in the JSON).
        gids = list(map(int, esearch_result['idlist'][0:max_genes]))

        # Do ESummary, db=gene, to get info about these genes; create Gene objects
        # ------------------------------------------------------------------------

        esummary_genes = esummary(gids, db = 'gene')
        rs.esummary_genes = esummary_genes  # for debugging
        my_genes = rs.my_genes = []
        my_genomic_infos = []
        my_location_hists = []
        gid_to_gene = {}   # cross reference a gene's UID to the Gene object

        for gid in gids:
            # FIXME: deal with error, when gid isn't found in JSON results
            esummary_gene = esummary_genes[str(gid)]

            try:
                g = Gene.objects.get(uid = gid, archived = False)
                debug_msg = "Updating "
            except Gene.DoesNotExist:
                g = Gene(uid=gid)
                debug_msg = "Creating new "

            # FIXME: deal with errors when expected keys are not found in the JSON
            g.name = esummary_gene['name']
            g.description = esummary_gene['description']
            g.chromosome = esummary_gene['chromosome']
            g.geneticsource = esummary_gene['geneticsource']
            org = esummary_gene['organism']
            g.organism_name = org['scientificname']
            g.organism_commonname = org['commonname']
            g.organism_taxid = org['taxid']
            g.summary = esummary_gene['summary']

            # First remove all existing GenomicInfo records for this gene
            GenomicInfo.objects.filter(gene = g).delete()
            # Now create new ones and add them
            for eginfo in esummary_gene['genomicinfo']:
                ginfo = GenomicInfo()
                ginfo.my_gene = g
                ginfo.chrloc = eginfo['chrloc']
                ginfo.chraccver = eginfo['chraccver']
                ginfo.chrstart = eginfo['chrstart']
                ginfo.chrstop = eginfo['chrstop']
                ginfo.exoncount = eginfo['exoncount']
                my_genomic_infos.append(ginfo)

            # Same, for LocationHist
            LocationHist.objects.filter(gene = g).delete()
            for elochist in esummary_gene['locationhist']:
                lochist = LocationHist()
                lochist.my_gene = g
                lochist.annotationrelease = elochist['annotationrelease']
                lochist.assemblyaccver = elochist['assemblyaccver']
                lochist.chraccver = elochist['chraccver']
                lochist.chrstart = elochist['chrstart']
                lochist.chrstop = elochist['chrstop']
                my_location_hists.append(lochist)

            logger.debug(debug_msg + str(g))
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
            print("linkset_gene: ")
            pp.pprint(linkset_gene)

            # Enforce max_genes here, too. This shouldn't be necessary, but doesn't hurt:
            if (gene_num >= max_genes): break

            # Get the gene id from the result, and look up the Gene object
            gid = linkset_gene['ids'][0]
            gene = gid_to_gene[gid]

            # Get protein ids as integers. Limit the number of proteins per gene
            if 'linksetdbs' in linkset_gene:
                gene_pids = list(map(int,
                    linkset_gene['linksetdbs'][0]['links'][0:max_proteins_per_gene]
                ))
                for pid in gene_pids:
                    pid_to_gene[pid] = gene
                pids.extend(gene_pids)

            gene_num = gene_num + 1

        # Do ESummary, db=protein, to get info about these proteins; create objects
        # -------------------------------------------------------------------------

        print('>>>>>>>>>> pids: ' + ",".join(map(str, pids)))
        esummary_proteins = esummary(pids, db = 'protein')
        rs.esummary_proteins = esummary_proteins   # for debugging
        proteins = rs.proteins = []
        for pid in pids:
            # FIXME: deal with error, when gid isn't found in JSON results
            esummary_protein = esummary_proteins[str(pid)]
            try:
                p = Protein.objects.get(uid = pid, archived = False)
                debug_msg = "Updating "
            except Protein.DoesNotExist:
                p = Protein(uid=pid)
                debug_msg = "Creating new "

            # FIXME: deal with errors when expected keys are not found in the JSON
            p.caption = esummary_protein['caption']
            p.title = esummary_protein['title']
            p.extra = esummary_protein['extra']
            p.gi = esummary_protein['gi']
            p.createdate = dateutil.parser.parse(esummary_protein['createdate'])
            p.updatedate = dateutil.parser.parse(esummary_protein['updatedate'])
            p.taxid = esummary_protein['taxid']
            p.slen = esummary_protein['slen']
            p.projectid = esummary_protein['projectid']
            p.genome = esummary_protein['genome']
            p.organism = esummary_protein['organism']

            logger.debug(debug_msg + str(p))
            proteins.append(p)


        # Save everything into the database, now that we've parsed all the 
        # E-utilities responses, and created all the
        # objects, with no errors.
        rs.save()
        for g in my_genes:
            g.save()
            rs.genes.add(g)

        for ginfo in my_genomic_infos:
            ginfo.gene = ginfo.my_gene
            ginfo.save()

        for lochist in my_location_hists:
            lochist.gene = lochist.my_gene
            lochist.save()

        for p in proteins:
            p.gene = pid_to_gene[p.uid]
            p.save()



        # FIXME - for now, we're not redirecting
        # Redirect to the page that will show the result.
        #return HttpResponseRedirect(reverse('gpt:result', args=(rs_id,)))

        return rs

    @classmethod
    def archive_it(cls, rsid):
        rs = cls.objects.get(pk = rsid)
        rs.archived = True
        rs.save()
        return rs



