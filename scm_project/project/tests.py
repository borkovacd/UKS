from django.test import TestCase
from django.contrib.auth.models import User
from project.models import Project, Problem, Milestone, Label
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
import json
from django.test.client import RequestFactory
from colorful.fields import RGBColorField
from project.views import ProjectDetailView

# Create your tests here.
class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='newUser', email='newUser@test.com', password='testing321')
        self.project = Project.objects.create(title="Project test", git_repository="https://github.com/olgaSavic/UKS",
                                              author=self.user)
        self.problem = Problem.objects.create(title="Problem test", description="Problem description test", project=self.project, reported_by=self.user)
        self.milestone = Milestone.objects.create(title ="Milestone test", description="Milestone description test", project=self.project)
        self.color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])
        self.client.login(username='newUser', password='testing321')
        self.client.user = self.user     
        self.date_created = timezone.now()
        self.due_date = timezone.now()     

    def test_create_milestone(self):
        milestone = Milestone.objects.create(title="Milestone1", description="Milestone1 description test",
                                     project=self.project)
        self.assertEqual(milestone.due_date, self.due_date)
        self.assertEqual(milestone.date_created, self.date_created)
        self.assertEqual(milestone.title, "Milestone1")
        self.assertEqual(milestone.description, "Milestone1 description test")
        self.assertEqual(milestone.project, self.project)

    def test_create_milestone_2(self):
    	response = self.client.post(reverse('milestone-create', kwargs={'pk' : self.project.id}), 
    		{'title':'New milestone', 'description':'New milestone description test', 'project': self.project})
    	self.assertEqual(response.status_code, 302)
    	count = Milestone.objects.all().count()
    	self.assertEqual(count, 2)
 		    
    def test_create_problem(self):
        problem = Problem.objects.create(title="Problem1", description="Problem1 description test", project=self.project, reported_by=self.user, milestone=self.milestone)
        self.assertEqual(problem.created_time, self.date_created)
        self.assertEqual(problem.title, "Problem1")
        self.assertEqual(problem.description, "Problem1 description test")
        self.assertEqual(problem.project, self.project)
        self.assertEqual(problem.milestone, self.milestone)
        self.assertEqual(problem.reported_by, self.user)

    def test_create_problem_2(self):
    	response = self.client.post(reverse('problem-create', kwargs={'pk' : self.project.id}), 
    		{'title':'New problem', 'description':'New problem description test', 'project': self.project})
    	self.assertEqual(response.status_code, 302)
    	count = Problem.objects.all().count()
    	self.assertEqual(count, 2)

    def test_update_milestone(self):
    	milestone = Milestone.objects.create(title="Test milestone", description="Description test milestone",
  			project=self.project)
    	response=self.client.post(reverse('milestone-update', kwargs={'pk': milestone.id}), {'title':'Test milestone 2', 'description':'Description test milestone 2',
  			'project': self.project})
    	self.assertEqual(response.status_code, 302)
    	milestone.refresh_from_db()
    	self.assertEqual(milestone.title, 'Test milestone 2')
    	self.assertEqual(milestone.description, 'Description test milestone 2')

    def test_delete_milestone(self):
    	milestone = Milestone.objects.create(title="Test milestone", description="Description test milestone",
  			project=self.project)
    	response = self.client.delete(reverse('milestone-delete', kwargs={'pk': milestone.id}))
    	self.assertEqual(response.status_code, 302)
    	count = Milestone.objects.filter(id=milestone.id).count()
    	self.assertEqual(count, 0)

    def test_delete_label(self):
    	label = Label.objects.create(title="Test label", description="Description test label",
  			project=self.project, color = self.color)
    	response = self.client.delete(reverse('label-delete', kwargs={'pk': label.id}))
    	self.assertEqual(response.status_code, 302)	
    	count = Label.objects.filter(id=label.id).count()
    	self.assertEqual(count, 0)


    def test_close_problem(self):
    	problem = Problem.objects.create(title="Problem1", description="Problem1 description test", project=self.project, reported_by=self.user, milestone=self.milestone)
    	response = self.client.post(reverse('close_problem', kwargs={'problem_id': problem.id}))
    	self.assertEqual(response.status_code, 302)
    	problem.refresh_from_db()
    	self.assertEqual(problem.opened, False)    

    def test_open_problem(self):
    	problem = Problem.objects.create(title="Problem1", description="Problem1 description test", project=self.project, reported_by=self.user, milestone=self.milestone)
    	response = self.client.post(reverse('open_problem', kwargs={'problem_id': problem.id}))
    	self.assertEqual(response.status_code, 302)
    	problem.refresh_from_db()
    	self.assertEqual(problem.opened, True) 	

    def test_link_milestone(self):
    	problem = Problem.objects.create(title="Problem1", description="Problem1 description test", 
    		project=self.project, reported_by=self.user)
    	milestone = Milestone.objects.create(title="Test milestone", description="Description test milestone",
  			project=self.project)
    	response = self.client.post(reverse('link_milestone', 
    		kwargs = {'problem_id' : problem.id, 'milestone_id' : milestone.id}))
    	self.assertEqual(response.status_code, 302)
    	problem.refresh_from_db()
    	self.assertEqual(problem.milestone, milestone)

    def test_unlink_milestone(self):
    	milestone = Milestone.objects.create(title="Test milestone unlink", description="Description test milestone",
  			project=self.project)
    	problem = Problem.objects.create(title="Problem1", description="Problem1 description test", 
    		project=self.project, reported_by=self.user, milestone=milestone)
    	response = self.client.post(reverse('unlink_milestone', 
    		kwargs = {'problem_id' : problem.id, 'milestone_id' : milestone.id}))
    	self.assertEqual(response.status_code, 302)
    	problem.refresh_from_db()
    	self.assertEqual(problem.milestone, None)

    		
		

    		


