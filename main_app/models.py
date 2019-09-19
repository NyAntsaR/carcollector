from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

#Field choices
CATEGORY = (
    ('R', 'Regular'),
    ('M', 'Midgrade'),
    ('P', 'Premium')
)

#-------- Create optional features model -------------------
class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('features_detail', kwargs={'pk': self.id})

#------------- Create car models ----------------------------
class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    year = models.IntegerField()
    features = models.ManyToManyField(Feature)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.make
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id' : self.id})
    
    def fuel_for_today(self):
        return self.gas_set.filter(date=date.today()).count() >= len(CATEGORY)

#------------- Create gas model -----------------------------
class Gas(models.Model):
    date = models.DateField('Car Fuel date')
    category = models.CharField(
        max_length=1,
            choices=CATEGORY,
            default='R'
    )

    #Adding foreign Key
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_category_display()} on {self.date}"
    
    # change the default sort
    class Meta:
        ordering = ['-date']


#------------- Create photo model -----------------------------
class Photo(models.Model):
    url = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for car_id: {self.car_id} @{self.url}"