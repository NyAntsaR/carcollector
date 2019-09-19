from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, DetailView, UpdateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Car, Feature, Photo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .forms import GasForm

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcoll1'

#--------- CAR CLASS -------------
class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['make', 'model', 'color', 'year']

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

class CarUpdate(UpdateView):
    model = Car
    fields = ['make', 'model', 'color', 'year']

class CarDelete(DeleteView):
    model = Car
    success_url = '/cars/'

#--------- CAR FUNCTION-------------
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cars_index(request):
    cars = Car.objects.filter(user=request.user)
    return render(request, 'cars/index.html', { 'cars' : cars })

def cars_detail(request, car_id):
  car = Car.objects.get(id=car_id)
  features_car_doesnt_have = Feature.objects.exclude(id__in = car.features.all().values_list('id'))
  gas_form = GasForm()
  return render(request, 'cars/detail.html', {
    'car': car, 
    'gas_form': gas_form,
    # Add the toys to be displayed
    'features': features_car_doesnt_have
  })

#--------- GAS -------------
def add_gas(request, car_id):
  # create the ModelForm using the data in request.POST
  form = GasForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    new_gas = form.save(commit=False)
    new_gas.car_id = car_id
    new_gas.save()
  return redirect('detail', car_id=car_id)

#--------- FEATURES CLASS -------------
class Featurelist(ListView):
  model = Feature

class FeatureDetail(DetailView):
  model = Feature

class FeatureCreate(CreateView):
  model = Feature
  fields = ['name', 'description']

class FeatureUpdate(UpdateView):
  model = Feature
  fields = ['name', 'description']

class FeatureDelete(DeleteView):
  model = Feature
  success_url = '/features/'

#---------- FEATURE FUNCTION ---------------- 
def assoc_feature(request, car_id, feature_id):
  Car.objects.get(id=car_id).features.add(feature_id)
  return redirect('detail', car_id=car_id)

def unassoc_feature(request, car_id, feautre_id):
  Car.objects.get(id=car_id).features.remove(feature_id)
  return redirect('detail', car_id=car_id)

#--------- ADD PHOTO -------------
def add_photo(request, car_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, car_id=car_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', car_id=car_id)

#--------- SIGN UP -------------
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)





