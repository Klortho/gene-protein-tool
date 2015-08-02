from django.db import models


class ResultSet(models.Model):
    last_updated = models.DateTimeField(auto_now = True)

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
        return "protein " + str(self.uid) + ": '" + self.title + "'"
