import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Member(models.Model):
	first_name = models.CharField(max_length=200, blank=True)
	last_name = models.CharField(max_length=200, blank=True)
	netid = models.CharField(max_length=100)
	company = models.ManyToManyField(Company)
	def __str__(self):
		if self.first_name and self.last_name:
			return "%s %s" % (self.first_name, self.last_name)
		return self.netid

class Admin(models.Model):
	member = models.ForeignKey(Member)
	company = models.ForeignKey(Company)