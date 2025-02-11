from django.contrib import admin
from .models import Specialization, District, Sub_district, HealthConcern
class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('name',)}
    list_display=['name', 'slug']

admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(HealthConcern)
admin.site.register(District)
admin.site.register(Sub_district)