
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    technologies = models.CharField(max_length=500, blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def get_technologies_list(self):
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Image for {self.project.title}"
    
    class Meta:
        ordering = ['order']


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    proficiency = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    company_logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg', 'webp'])]
    )
    description = models.TextField()
    start_date = models.CharField(max_length=50)  # Using CharField temporarily
    end_date = models.CharField(max_length=50, blank=True, null=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"
    
    
class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    score = models.CharField(max_length=100)
    year = models.CharField(max_length=50)

    def __str__(self):
        return self.degree


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    completion_date = models.CharField(max_length=50)

    def __str__(self):
        return self.title
