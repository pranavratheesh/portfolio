from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Skill, Experience, Education, Certification,ProjectImage



@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency']
    list_filter = ['category']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'title', 'start_date', 'current', 'logo_thumbnail']
    list_filter = ['current']
    search_fields = ['company', 'title']
    
    # Optional: Add fields to show in edit form
    fields = ['company', 'company_logo', 'title', 'description', 
              'start_date', 'end_date', 'current']
    
    def logo_thumbnail(self, obj):
        if obj.company_logo:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 5px; object-fit: contain;" />',
                obj.company_logo.url
            )
        return "No logo"
    logo_thumbnail.short_description = 'Logo'

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'year']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'completion_date']

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ['title', 'featured', 'created_at']