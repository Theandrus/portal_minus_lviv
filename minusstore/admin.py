from django.contrib import admin
from minusstore.models import (
    MinusstoreMinuscategory,
    MinusstoreMinusplusrecord,
    MinusstoreMinusauthor,
    MinusstoreMinusrecord,
    MinusstoreMinusweekstats,
    MinusstoreMinusstopword,
    MinusstoreMinusstats,
    Minusgenre,
    Minusappointment,
)

@admin.register(MinusstoreMinuscategory)
class MinusstoreMinuscategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(MinusstoreMinusplusrecord)
class MinusstoreMinusplusrecordAdmin(admin.ModelAdmin):
    pass

@admin.register(MinusstoreMinusauthor)
class MinusstoreMinusauthorAdmin(admin.ModelAdmin):
    pass

@admin.register(MinusstoreMinusrecord)
class MinusstoreMinusrecordAdmin(admin.ModelAdmin):
    pass

@admin.register(MinusstoreMinusweekstats)
class MinusstoreMinusweekstatsAdmin(admin.ModelAdmin):
    pass

@admin.register(MinusstoreMinusstopword)
class MinusstoreMinusstopwordAdmin(admin.ModelAdmin):
    pass

@admin.register(MinusstoreMinusstats)
class MinusstoreMinusstatsAdmin(admin.ModelAdmin):
    pass

@admin.register(Minusgenre)
class MinusgenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Minusappointment)
class MinusappointmentAdmin(admin.ModelAdmin):
    pass
