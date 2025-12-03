from django.core.management.base import BaseCommand
from portfolioapp.models import Project, Skill, Experience, Education, Certification

class Command(BaseCommand):
    help = 'Populate initial data for portfolio'

    def handle(self, *args, **options):
        # Clear existing data
        Project.objects.all().delete()
        Skill.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()
        Certification.objects.all().delete()

        # Add projects
        Project.objects.create(
            title="Women Safety Scream Alarm",
            short_description="Women Security App with Scream Alert designed to enhance personal safety",
            description="Women Security App with Scream Alert is designed to enhance personal safety for women by providing an automatic, real-time distress signaling solution. Key features: Real-time Sound producing, GPS Integration, Manual Panic Button for activating the alert",
            technologies="Python, Django, React, GPS API",
            featured=True
        )
        
        Project.objects.create(
            title="MovieCupid",
            short_description="Personalized movie recommendation platform",
            description="A personalized movie recommendation platform that identifies users' favorite genres, artists, and directors to suggest movies tailored to their interests. It integrates external movie database TMDb to fetch details about movies, reviews, ratings, and OTT availability.",
            technologies="Django, HTML/CSS, TMDb API, PostgreSQL",
            featured=True
        )

        # Add skills
        skills_data = [
            ('Python', 'Backend', 85),
            ('Django', 'Backend', 80),
            ('Flask', 'Backend', 70),
            ('React', 'Frontend', 75),
            ('HTML/CSS', 'Frontend', 85),
            ('JavaScript', 'Frontend', 75),
            ('MySQL', 'Database', 80),
            ('PostgreSQL', 'Database', 75),
            ('API Integration', 'Backend', 80),
        ]
        
        for name, category, proficiency in skills_data:
            Skill.objects.create(
                name=name,
                category=category,
                proficiency=proficiency
            )

        # Add experiences
        Experience.objects.create(
            title="Intern",
            company="Luminar Technolab",
            description="Pursuing a full stack course in Python Django and React with hands-on web development experience.",
            start_date="Oct 2023",
            current=True
        )
        
        Experience.objects.create(
            title="Intern",
            company="Tech By Heart",
            description="Gained hands-on experience in cybersecurity and learned to combat digital threats.",
            start_date="Dec 2023",
            end_date="Jan 2024"
        )

        # Add education
        Education.objects.create(
            degree="Bachelor of Science in Computer Science",
            institution="University Name",
            score="CGPA 7.0",
            year="2020-2023"
        )
        
        Education.objects.create(
            degree="Higher Secondary Education",
            institution="School Name",
            score="Aggregate: 85%",
            year="2018-2020"
        )

        # Add certifications
        Certification.objects.create(
            title="Python Django - React - Full Stack Web Development Expert",
            issuer="Luminar Technolab",
            completion_date="Oct 2025"
        )
        
        Certification.objects.create(
            title="Cyber Security Intern",
            issuer="Tech By Heart",
            completion_date="Dec 2023"
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))