from django.contrib.auth.models import User
from django.db import models

import dateutil.parser
import logging
import pprint

from gpt.eutils import *
from project.settings import GPT


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
    chrloc = models.CharField(max_length=20)
    chraccver = models.CharField(max_length=20)
    chrstart = models.IntegerField(null=True)
    chrstop = models.IntegerField(null=True)
    exoncount = models.IntegerField(null=True)

class LocationHist(models.Model):
    gene = models.ForeignKey(Gene)
    annotationrelease = models.CharField(max_length=20)
    assemblyaccver = models.CharField(max_length=30)
    chraccver = models.CharField(max_length=20)
    chrstart = models.IntegerField(null=True)
    chrstop = models.IntegerField(null=True)


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

# This convenience function gets a string value for a key in a json object,
# if that key exists. If not, it returns the empty string
def _get_string(json, k):
    return json[k] if k in json else ""

# ResultSet model

class ResultSet(models.Model):
    user = models.ForeignKey(User)
    last_updated = models.DateTimeField(auto_now = True)
    genes = models.ManyToManyField(Gene)
    query = models.CharField(max_length = 200)
    archived = models.BooleanField(default = False)

    # Create a new ResultSet from an Entrez query string.
    # This does not save the ResultSet, or any of the resultant Gene or
    # Protein objects, into the database.
    @classmethod
    def create_from_query(cls, query, user):
        try:
            rs = cls.objects.get(query=query, user=user, archived=False)
            debug_msg = "Updating "
        except cls.DoesNotExist:
            rs = cls(query=query, user=user)
            debug_msg = "Creating new "

        logger.debug(debug_msg + str(rs))

        # Lists for storing the child model objects we create. If all goes well
        # then all of these get saved to the DB at the end
        my_genes = []
        my_genomic_infos = []
        my_location_hists = []
        proteins = []

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

        if len(gids) > 0:
            esummary_genes = esummary(gids, db = 'gene')
            gid_to_gene = {}   # cross reference a gene's UID to the Gene object

        for gid in gids:
            # FIXME: deal with error, when gid isn't found in JSON results
            eg = esummary_genes[str(gid)]

            try:
                g = Gene.objects.get(uid = gid, archived = False)
                debug_msg = "Updating "
            except Gene.DoesNotExist:
                g = Gene(uid=gid)
                debug_msg = "Creating new "

            g.name = _get_string(eg, 'name')
            g.description = _get_string(eg, 'description')
            g.chromosome = _get_string(eg, 'chromosome')
            g.geneticsource = _get_string(eg, 'geneticsource')
            if 'organism' in eg:
                org = eg['organism']
                g.organism_name = _get_string(org, 'scientificname')
                g.organism_commonname = _get_string(org, 'commonname')
                g.organism_taxid = _get_string(org, 'taxid')
                g.summary = _get_string(eg, 'summary')

            # First remove all existing GenomicInfo records for this gene
            GenomicInfo.objects.filter(gene = g).delete()

            # Now create new ones and add them
            for eginfo in eg['genomicinfo']:
                ginfo = GenomicInfo()
                ginfo.my_gene = g
                ginfo.chrloc = _get_string(eginfo, 'chrloc')
                ginfo.chraccver = _get_string(eginfo, 'chraccver')
                if 'chrstart' in eginfo:
                    ginfo.chrstart = eginfo['chrstart']
                if 'chrstop' in eginfo:
                    ginfo.chrstop = eginfo['chrstop']
                if 'exoncount' in eginfo:
                    ginfo.exoncount = eginfo['exoncount']
                my_genomic_infos.append(ginfo)

            # Same, for LocationHist
            LocationHist.objects.filter(gene = g).delete()
            for elochist in eg['locationhist']:
                lochist = LocationHist()
                lochist.my_gene = g
                lochist.annotationrelease = _get_string(elochist, 'annotationrelease')
                lochist.assemblyaccver = _get_string(elochist, 'assemblyaccver')
                lochist.chraccver = _get_string(elochist, 'chraccver')
                if 'chrstart' in elochist:
                    lochist.chrstart = elochist['chrstart']
                if 'chrstop' in elochist:
                    lochist.chrstop = elochist['chrstop']
                my_location_hists.append(lochist)

            logger.debug(debug_msg + str(g))
            my_genes.append(g)
            gid_to_gene[gid] = g

        # Do ELink to get all the proteins associated with each of these genes
        # --------------------------------------------------------------------

        if len(gids) > 0:
            elink_result = elink(gids, 
                                 dbfrom='gene', 
                                 db='protein', 
                                 linkname='gene_protein')

            # The elink results come back grouped by gene. Iterate over each gene, and
            # aggregate all the protein ids into one list. Also create a dictionary
            # to cross-reference pid to the Gene object
            pids = []
            pid_to_gene = {}
            gene_num = 0
            for linkset_gene in elink_result:
                #print("linkset_gene: ")
                #pp.pprint(linkset_gene)

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

            if len(pids) > 0:
                esummary_proteins = esummary(pids, db = 'protein')

            for pid in pids:
                # FIXME: deal with error, when gid isn't found in JSON results
                ep = esummary_proteins[str(pid)]
                try:
                    p = Protein.objects.get(uid = pid, archived = False)
                    debug_msg = "Updating "
                except Protein.DoesNotExist:
                    p = Protein(uid=pid)
                    debug_msg = "Creating new "


                p.caption = _get_string(ep, 'caption')
                p.title = _get_string(ep, 'title')
                p.extra = _get_string(ep, 'extra')
                if ('gi' in ep): 
                    p.gi = ep['gi']
                if ('createdate' in ep):
                    p.createdate = dateutil.parser.parse(ep['createdate'])
                if ('updatedate' in ep):
                    p.updatedate = dateutil.parser.parse(ep['updatedate'])
                if ('taxid' in ep):
                    p.taxid = ep['taxid']
                if ('slen' in ep):
                    p.slen = ep['slen']
                p.projectid = _get_string(ep, 'projectid')
                p.genome = _get_string(ep, 'genome')
                p.organism = _get_string(ep, 'organism')

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

        return rs

    @classmethod
    def archive_it(cls, rsid):
        rs = cls.objects.get(pk = rsid)
        rs.archived = True
        rs.save()
        return rs



