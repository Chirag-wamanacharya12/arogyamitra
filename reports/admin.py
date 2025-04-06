from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'file_preview')
    search_fields = ('title',)
    readonly_fields = ('uploaded_at',)

    def file_preview(self, obj):
        if obj.file and obj.file.name.endswith('.pdf'):
            return f"<a href='{obj.file.url}' target='_blank'>Preview PDF</a>"
        elif obj.file:
            return f"<a href='{obj.file.url}' target='_blank'>Download</a>"
        return "No file"
    file_preview.allow_tags = True
    file_preview.short_description = "Preview"
