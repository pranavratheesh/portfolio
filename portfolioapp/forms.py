# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import 


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your message',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message here...',
                'rows': 6,
                'required': True
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Message'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Basic email validation
        if not email:
            raise ValidationError("Email is required")
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise ValidationError("Message must be at least 10 characters long")
        return message

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['title', 'bio', 'profile_picture', 'email', 'phone', 'location', 'resume']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Full Stack Developer'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a compelling bio about yourself...',
                'rows': 5
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }
        labels = {
            'profile_picture': 'Profile Picture',
            'resume': 'Resume/CV'
        }

class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url', 'icon_class']
        widgets = {
            'platform': forms.Select(attrs={
                'class': 'form-control'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/your-profile'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fab fa-github (Font Awesome class)'
            }),
        }

SocialLinkFormSet = forms.inlineformset_factory(
    Profile, SocialLink, 
    form=SocialLinkForm,
    extra=1,
    can_delete=True
)

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'proficiency', 'icon', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python, React, AWS'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'proficiency': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100,
                'type': 'range'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fab fa-python (Font Awesome class)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }

    def clean_proficiency(self):
        proficiency = self.cleaned_data.get('proficiency')
        if proficiency < 1 or proficiency > 100:
            raise ValidationError("Proficiency must be between 1 and 100")
        return proficiency

SkillFormSet = forms.inlineformset_factory(
    Profile, Skill,
    form=SkillForm,
    extra=1,
    can_delete=True
)

class ProjectForm(forms.ModelForm):
    technologies = forms.ModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'technology-checkboxes'
        }),
        required=False
    )
    
    class Meta:
        model = Project
        fields = [
            'title', 'short_description', 'description', 'project_type',
            'featured_image', 'github_url', 'live_url', 'technologies',
            'featured', 'start_date', 'end_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Title'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description (max 300 characters)',
                'maxlength': 300
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed project description...',
                'rows': 8
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/project'
            }),
            'live_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://your-project.com'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'featured': 'Mark as Featured Project',
            'github_url': 'GitHub Repository URL',
            'live_url': 'Live Demo URL'
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date")
        
        return cleaned_data

    def clean_short_description(self):
        short_description = self.cleaned_data.get('short_description')
        if len(short_description) > 300:
            raise ValidationError("Short description must be 300 characters or less")
        return short_description

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image caption...'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }

ProjectImageFormSet = forms.inlineformset_factory(
    Project, ProjectImage,
    form=ProjectImageForm,
    extra=3,
    can_delete=True
)

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'icon', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., React, Django, PostgreSQL'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fab fa-react (Font Awesome class)'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Frontend, Backend, Database'
            }),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            'company', 'company_logo', 'title', 'description',
            'start_date', 'end_date', 'current'
        ]
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
            'company_logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Position/Role'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'current': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your responsibilities and achievements...',
                'rows': 6
            }),
        }
        labels = {
            'current': 'I currently work here',
            'company_logo': 'Company Logo (Optional)'
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        current = cleaned_data.get('current')
        
        if current and end_date:
            raise forms.ValidationError("Cannot have both end date and current position checked")
        
        if not current and not end_date:
            raise forms.ValidationError("Either set end date or mark as current position")
        
        # Convert to date objects if they're strings for comparison
        if end_date and start_date:
            try:
                from datetime import datetime
                start = datetime.strptime(str(start_date), '%Y-%m-%d')
                end = datetime.strptime(str(end_date), '%Y-%m-%d')
                if end < start:
                    raise forms.ValidationError("End date cannot be before start date")
            except ValueError:
                # If dates are in different format, skip validation
                pass
        
        return cleaned_data
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            'institution', 'degree', 'field_of_study',
            'start_date', 'end_date', 'current', 'description', 'grade'
        ]
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'University/School Name'
            }),
            'degree': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bachelor of Science'
            }),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'current': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional information about your education...',
                'rows': 4
            }),
            'grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3.8 GPA, First Class Honors'
            }),
        }
        labels = {
            'current': 'I currently study here'
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        current = cleaned_data.get('current')
        
        if current and end_date:
            raise ValidationError("Cannot have both end date and current education checked")
        
        if not current and not end_date:
            raise ValidationError("Either set end date or mark as current education")
        
        if end_date and start_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date")
        
        return cleaned_data

EducationFormSet = forms.inlineformset_factory(
    Profile, Education,
    form=EducationForm,
    extra=1,
    can_delete=True
)

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'issuing_organization', 'issue_date', 'expiration_date', 'credential_id', 'credential_url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certificate Name'
            }),
            'issuing_organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Issuing Organization'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'credential_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Credential ID (if any)'
            }),
            'credential_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL to verify certificate'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        expiration_date = cleaned_data.get('expiration_date')
        
        if expiration_date and issue_date and expiration_date < issue_date:
            raise ValidationError("Expiration date cannot be before issue date")
        
        return cleaned_data

CertificateFormSet = forms.inlineformset_factory(
    Profile, Certificate,
    form=CertificateForm,
    extra=1,
    can_delete=True
)

class BlogPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'tag-checkboxes'
        }),
        required=False
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'slug', 'excerpt', 'content', 'featured_image',
            'status', 'published_date', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Blog Post Title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'url-friendly-slug'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief excerpt for preview...',
                'rows': 3,
                'maxlength': 300
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 15
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'published_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        # Basic slug validation
        if not slug.replace('-', '').isalnum():
            raise ValidationError("Slug can only contain letters, numbers, and hyphens")
        return slug

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        if len(excerpt) > 300:
            raise ValidationError("Excerpt must be 300 characters or less")
        return excerpt

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tag Name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'tag-slug'
            }),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            'client_name', 'client_position', 'client_company',
            'client_image', 'content', 'rating', 'featured'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client Name'
            }),
            'client_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client Position'
            }),
            'client_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client Company'
            }),
            'client_image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Testimonial content...',
                'rows': 5
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'featured': 'Featured Testimonial'
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5")
        return rating

TestimonialFormSet = forms.inlineformset_factory(
    Profile, Testimonial,
    form=TestimonialForm,
    extra=1,
    can_delete=True
)

# Search Form
class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search projects, blog posts, skills...',
            'aria-label': 'Search'
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('projects', 'Projects'),
            ('blog', 'Blog Posts'),
            ('skills', 'Skills')
        ],
        required=False,
        initial='all',
        widget=forms.RadioSelect(attrs={
            'class': 'search-type-radio'
        })
    )

# Newsletter Subscription Form
class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email for updates',
            'required': True
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add any additional validation (e.g., check if already subscribed)
        return email

# Project Filter Form
class ProjectFilterForm(forms.Form):
    PROJECT_TYPE_CHOICES = [('', 'All Types')] + Project.PROJECT_TYPES
    
    project_type = forms.ChoiceField(
        choices=PROJECT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    technology = forms.ModelChoiceField(
        queryset=Technology.objects.all(),
        required=False,
        empty_label="All Technologies",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'this.form.submit()'
        })
    )
    
    featured = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'this.form.submit()'
        }),
        label='Featured Only'
    )

# Comment Form for Blog Posts
class CommentForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email (will not be published)',
            'required': True
        })
    )
    
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your comment...',
            'rows': 4,
            'required': True
        })
    )
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment.strip()) < 10:
            raise ValidationError("Comment must be at least 10 characters long")
        return comment