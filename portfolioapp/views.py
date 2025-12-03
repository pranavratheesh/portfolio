
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Project, ProjectImage, Skill, Experience, Education, Certification
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.urls import reverse


class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Your personal data
        personal_info = {
            'name': 'Pranav C',
            'title': 'Full Stack Web Developer (Python Django / React)',
            'phone': '+917736707020',
            'email': 'pranavc493@gmail.com',
            'location': 'India',
            'github': 'https://github.com/pranavratheesh',
            'summary': 'Recent B.Sc. Computer Science graduate with a strong foundation in Python, Django, HTML, CSS, JavaScript, API integration, and SQL. Completed internships at Luminar Technolab and Tech By Heart, gaining practical experience in full-stack web development and backend integration.'
        }
        
        context['personal_info'] = personal_info
        
        # Get projects with their first image for the homepage
        featured_projects = Project.objects.filter(featured=True)[:3]
        all_projects = Project.objects.all()[:6]
        
        context['featured_projects'] = featured_projects
        context['projects'] = all_projects
        context['skills'] = Skill.objects.all()
        context['experiences'] = Experience.objects.all().order_by('-id')
        context['education'] = Education.objects.all()
        context['certifications'] = Certification.objects.all()
        
        return context


class ProjectsListView(ListView):
    model = Project
    template_name = 'main/projects.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        # Get all projects, ordered by creation date (newest first)
        # Prefetch related images for performance
        return Project.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add featured projects to context
        context['featured_projects'] = Project.objects.filter(featured=True).order_by('-created_at')
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'main/project_detail.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'
    
    def get_object(self):
        """Get the project object or return 404"""
        project_id = self.kwargs.get('project_id')
        # Get project with prefetched images for better performance
        project = get_object_or_404(
            Project.objects.prefetch_related('images'), 
            id=project_id
        )
        return project
    
    def get_context_data(self, **kwargs):
        """Add extra context data"""
        context = super().get_context_data(**kwargs)
        project = self.object
        
        # Get all images for this project (already prefetched)
        # They're available in template as project.images.all()
        
        # Add related projects (exclude current project)
        # Prefetch images for related projects too
        context['related_projects'] = Project.objects.exclude(
            id=project.id
        ).prefetch_related('images')[:3]
        
        return context


# Add these helper views for better UX
def redirect_to_project_detail(request, project_id):
    """Redirect from old URLs if needed"""
    return redirect('project_detail', project_id=project_id)


def project_quick_view(request, project_id):
    """Quick view modal content (optional)"""
    project = get_object_or_404(
        Project.objects.prefetch_related('images'), 
        id=project_id
    )
    return render(request, 'main/partials/project_quick_view.html', {'project': project})


# Optional: View to handle image gallery management
def manage_project_images(request, project_id):
    """View to manage images for a project (requires authentication)"""
    project = get_object_or_404(Project, id=project_id)
    images = project.images.all().order_by('order')
    
    context = {
        'project': project,
        'images': images,
    }
    
    return render(request, 'main/manage_images.html', context)


# Function-based views as fallback (optional)
def index(request):
    view = IndexView()
    return view.dispatch(request)


def projects(request):
    view = ProjectsListView()
    return view.dispatch(request)


def project_detail(request, project_id):
    view = ProjectDetailView()
    return view.dispatch(request, project_id=project_id)
