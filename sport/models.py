from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import datetime

GENERIC_SAFETY_REGULATIONS = 'Please maintain social distancing and maintain COVID guidelines at all times. Any nuisance is punishable.'

def is_future_date(date):
  if date < datetime.date.today():
    raise ValidationError(
      _('%(date)s must be a future date!'),
      params = {'date': date}
    )

def less_than_six(number):
  if number > 5 or number < 1:
    raise ValidationError(
      _('%(number) must be between 1 to 5'),
      params = {'number': number}
    )

class Sport(models.Model):
  name = models.CharField(max_length=300)
  description = models.TextField(blank=True, null=True)
  coordinator = models.CharField(max_length=200)
  POCEmail = models.EmailField(max_length=200, default='deanbsa@iitd.ac.in')
  # note: In new database, this MUST NOT be nullable
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return u'{0}'.format(self.name)

class Facility(models.Model):
  sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
  name = models.CharField(max_length=300)
  type = models.CharField(max_length=20, default="Court")
  location = models.CharField(max_length=100, default="SAC")
  google_map_link = models.URLField(blank=True, null=True)
  capacity = models.IntegerField(default=300)
  inventory = models.CharField(max_length=200, null=True, blank=True)
  remarks = models.CharField(max_length=200, null=True, blank=True)
  safety_regulations = models.CharField(max_length=300, default=GENERIC_SAFETY_REGULATIONS)

  created_by = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return u'{0}'.format(self.name)

class Slot(models.Model):
  sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
  facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
  duration = models.FloatField(default=60)
  timeStart = models.TimeField()
  timeEnd = models.TimeField()
  date = models.DateField(validators=[is_future_date])
  is_booked = models.BooleanField(default=False)
  is_reviewed = models.BooleanField(default=False)
  booked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
  booked_at = models.DateTimeField(null=True, blank=True)

  created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='staff')
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)

class Review(models.Model):
  slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
  rating = models.IntegerField(validators=[less_than_six])
  review = models.CharField(max_length=300)

  created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reviewer')
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)
