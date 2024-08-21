from django.contrib import admin
from .models import Apply,DoneApply,CompanyInfo

# Register your models here.
# admin.site.register(apply)

admin.site.register(CompanyInfo)
admin.site.register(DoneApply)


@admin.register(Apply)
class ApplyAdmin(admin.ModelAdmin):
    field_names = tuple([f.name for f in Apply._meta.get_fields()])
    list_display = field_names
    list_filter = ('apply_at',)
