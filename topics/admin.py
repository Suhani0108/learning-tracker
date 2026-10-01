from django.contrib import admin

from .models import Resource, Topic


# An "inline" shows a topic's resources inside the topic's edit page
class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1  # one empty row for adding a new resource


# The @admin.register decorator adds Topic to the admin site at /admin/
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    # Columns shown in the list of topics
    list_display = ("title", "owner", "status", "updated_at", "created_at")
    # Sidebar filters
    list_filter = ("status", "owner")
    # Search box that looks inside these fields
    search_fields = ("title", "description")
    inlines = [ResourceInline]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "url", "created_at")
    search_fields = ("title", "url")
