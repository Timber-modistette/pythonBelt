from __future__ import unicode_literals
import datetime
from django.db import models
import re
# Create your models here.

class UserManager(models.Manager):
	def validateUser(self,post):
		is_valid = True
		errors =[]
		
		if len(post.get('first_name')) == 0:
			is_valid = False
			errors.append("Must enter valid name")

		if len(post.get('last_name')) == 0:
			is_valid = False
			errors.append("Must enter valid last name")

		if not re.search(r'\w+\@+\w+\.\w+', post.get('email')):
			is_valid = False
			errors.append("Please enter a valid email address")

		if User.objects.filter(email=post.get('email')).first() != None:
			is_valid = False
			errors.append("email already exists")

		if len(post.get('password')) < 6:
			is_valid = False
			errors.append("please enter a password of at least 6 characters")

		if post.get('password') != post.get('cf_password'):
			is_valid = False
			errors.append("passwords do not match")

		if len(post.get('dob')) != 10:
			errors.append("Please enter valid Date of Birth")
			print len(post.get('dob'))

		if len(post.get('dob')) == 10:
			dob = str(post.get('dob'))
			dob_conversion =datetime.datetime.strptime(dob,'%Y-%m-%d').date()
			now = datetime.datetime.now().date()
			delta = dob_conversion-now
			print delta


			if delta.days > 0:
				is_valid = False
				errors.append("future birthdate listed")
			if abs(delta.days) < 6570:
				is_valid= False
				errors.append('must be 18 years or older')


		return (is_valid, errors)


class User(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=200)
	password = models.CharField(max_length=100)
	cf_password = models.CharField(max_length=100)
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

# class QuoteManager(models.Manager):
# 	def validateQuote(self, post):
# 		is_valid = True
# 		errors = []

# 		if len(post.get('quoted_by')) < 3:
# 			is_valid = False
# 			errors.append("Quoted By must contain at least 3 characters")
# 		if len(post.get('content')) < 10:
# 			is_valid = False
# 			errors.append("Quote must contain at least 10 characters")

# 		return (is_valid, errors)




class Quote(models.Model):
	quoted_by = models.CharField(max_length=255)
	content = models.CharField(max_length=255)
	user = models.ForeignKey(User, related_name='quotes')
	favourites = models.ManyToManyField(User, related_name='favourited_quotes')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# objects = QuoteManager()



