from django.contrib import admin

from .models import Board, Critique, Profile, Reference, Shot, ShotMatch


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "skill_level", "camera")
    list_filter = ("skill_level",)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("pexels_id", "photographer", "alt_text")
    search_fields = ("photographer", "alt_text")


class ShotMatchInline(admin.TabularInline):
    model = ShotMatch
    extra = 0


class CritiqueInline(admin.StackedInline):
    model = Critique
    extra = 0


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "settings_summary", "created_at")
    list_filter = ("owner", "created_at")
    search_fields = ("title", "idea_text")
    fieldsets = (
        (None, {"fields": ("owner", "title", "image", "idea_text", "keywords")}),
        ("Camera settings (EXIF)", {
            "fields": (("aperture", "shutter_speed"), ("iso", "focal_length")),
        }),
    )
    inlines = [ShotMatchInline, CritiqueInline]


@admin.register(Critique)
class CritiqueAdmin(admin.ModelAdmin):
    list_display = ("shot", "model_name", "created_at")
    list_filter = ("model_name",)


@admin.register(ShotMatch)
class ShotMatchAdmin(admin.ModelAdmin):
    list_display = ("shot", "reference", "similarity", "rank")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "shoot_date", "location", "reference_count")
    list_filter = ("owner", "shoot_date")
    search_fields = ("name", "description", "location")
    fields = ["owner", "name", "description", ("shoot_date", "location"), "references"]
    filter_horizontal = ("references",)
