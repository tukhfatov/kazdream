from django.db import models

# Create your models here.
class Vacancy(models.Model):
	page = models.IntegerField()
	title = models.CharField(max_length=150)
	employer = models.CharField(max_length=100)
	contact_person = models.CharField(max_length=150)
	telephone = models.CharField(max_length=30)
	email = models.EmailField()
	
	city = models.CharField(max_length=150)
	salary = models.CharField(max_length=30)
	working_place = models.CharField(max_length=200)
	working_hours = models.CharField(max_length=150)
	condition = models.TextField()
	responsibility = models.TextField()

	education = models.CharField(max_length=200)
	experience = models.CharField(max_length=200)
	requirements = models.TextField()

	class Meta:
		db_table = 'md_vacancy'
