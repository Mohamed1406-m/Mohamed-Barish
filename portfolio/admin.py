from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Project, StackItem


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("name", "title", "location", "email", "linkedin", "photo")}),
        ("Hero Section", {"fields": ("hero_headline", "hero_sub")}),
        ("Stats Bar", {"fields": ("years_exp", "corps_count", "apps_count", "ai_label")}),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:60px;border-radius:50%">', obj.photo.url)
        return "—"
    photo_preview.short_description = "Photo"
    readonly_fields = ("photo_preview",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("order", "client", "title", "highlight", "is_active", "image_preview")
    list_editable = ("order", "highlight", "is_active")
    list_display_links = ("title",)
    search_fields = ("client", "title")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:48px;border-radius:6px">', obj.image.url)
        return "—"
    image_preview.short_description = "Image"


@admin.register(StackItem)
class StackItemAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "is_active")
    list_display_links = ("name",)
    list_editable = ("order", "is_active")


admin.site.site_header = "Barish Portfolio Admin"
admin.site.site_title = "Portfolio"
admin.site.index_title = "Manage your portfolio content"
