from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import datetime
import pytz 
from django.db.models import Count



def current_user(request):
	return User.objects.get(id=request.session['user_id'])


def index(request):
	print ('INDEX')

	return render(request, 'first_app/index.html')

def register(request):
	print ('REGISTER')
	if request.method != 'POST':
		return redirect('/')
	else:
		
		dob = str(request.POST['dob'])
	 
		check = User.objects.validateUser(request.POST)
		if check[0] == False:
			for errors in check[1]:
				messages.error(request, errors)

			return redirect('/')
		else:
			dob = str(request.POST['dob'])
			dob_conversion =datetime.datetime.strptime(dob,'%Y-%m-%d').date()
			hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
			user = User.objects.create(first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'), email=request.POST.get('email'), password=hashed_pw, dob=dob_conversion )
			request.session['user_id'] = user.id
			request.session['name'] =user.first_name
			
	return redirect('/homepage')



def login(request):
	print ('LOGIN')
	if request.method != 'POST':
		return redirect('/')
	else:
		if request.POST.get('email') == '' or request.POST.get('password') == '':
			messages.error(request, "no")
			return redirect('/')

		user = User.objects.filter(email=request.POST.get('email')).first()
		if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
			request.session['user_id']= user.id
			request.session['name']= user.first_name
			

			return redirect('/homepage')
		else:
			messages.error(request, "Please check info and try again or please register")
			return redirect('/')


def homepage(request):
	print ('homepage')
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		
		context = {'quotes': Quote.objects.exclude(favourites=current_user(request)).order_by('-created_at').all()[0:], 'current_user':current_user(request)}


		return render(request, 'first_app/homepage.html', context)


def logout(request):
	print ('logout')

	request.session.delete()


	return redirect('/')

def createQuote(request):
	print ('createquote')
	if request.method != 'POST':
		return redirect('/')
	else:
		if len(request.POST.get('quoted_by')) < 3:
			messages.error(request, "Quoted by must contain at least 3 characters")
			return redirect('/homepage')
		if len(request.POST.get('content')) < 10:
			messages.error(request, "Quote must contain at least 3 characters")
			return redirect('/homepage')
		else:
# 			is_valid = False
# 			errors.append("Quoted By must contain at least 3 characters")

		# check = Quote.objects.validateQuote(request.POST)
		# if check[0] == False:
		# 	for errors in check[1]:
		# 		messages.error(request, errors)
		# 	return('/homepage')
		# else:
		# yes i know youre going to minus points for making a big fat views in stead of models
		# BUT as you see i TRRIED to put in the models and it kept erroring
		#saying that something didnt have a str object idk. 

			quote = Quote.objects.create(quoted_by=request.POST['quoted_by'], content=request.POST['content'], user=current_user(request))


			return redirect('/homepage')

def favouritequote(request,quoteid):
	print ('favs')
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		getQuote = Quote.objects.get(id=quoteid)

		quote = getQuote.favourites.add(current_user(request))



	return redirect('/homepage')

def userProfile(request, userid):
	print('userprofile')
	if 'user_id' not in request.session:
		return redirect('/')
	else:

		user = User.objects.annotate(num_quotes=Count('quotes')).get(id=userid)
		
		context = {'user':user}



	return render(request, 'first_app/user.html', context)



def removequote(request, quoteid):
	print('removequote')
	if 'user_id' not in request.session:
		return	redirect('/')
	else:

		quote = Quote.objects.get(id=quoteid)

		remove = quote.favourites.remove(current_user(request))




	return	redirect('/homepage')

