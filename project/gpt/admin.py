from django.contrib import admin

# Register your models here.
from .models import ResultSet, Gene, Protein

class ProteinInline(admin.StackedInline):
    model = Protein
    extra = 3

class GeneAdmin(admin.ModelAdmin):
    inlines = [ProteinInline]

admin.site.register(Gene, GeneAdmin)


admin.site.register(ResultSet)

