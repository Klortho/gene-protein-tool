from django.contrib import admin

# Register your models here.
from .models import *

class GenomicInfoInline(admin.StackedInline):
    model = GenomicInfo
    extra = 0

class LocationHistInline(admin.StackedInline):
    model = LocationHist
    extra = 0

class ProteinInline(admin.StackedInline):
    model = Protein
    extra = 0

class GeneAdmin(admin.ModelAdmin):
    #fields = ['name', 'description']
    inlines = [GenomicInfoInline, LocationHistInline, ProteinInline]


admin.site.register(ResultSet)
admin.site.register(Gene, GeneAdmin)


