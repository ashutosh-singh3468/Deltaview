from django.contrib import admin

from .models import ComparisonResult


@admin.register(ComparisonResult)
class ComparisonResultAdmin(admin.ModelAdmin):
    list_display = ('left_file_name', 'right_file_name', 'similarity_percent', 'created_at')
    readonly_fields = ('created_at',)
