from django import forms
import time
from sport.models import Facility, Slot, Sport

class CreateNewSportForm(forms.ModelForm):
  class Meta:
    model = Sport
    fields = (
      'name',
      'description',
      'coordinator',
      'POCEmail'
    )

  def __init__(self, *args, **kwargs):
    super(CreateNewSportForm, self).__init__(*args, **kwargs)
    for field in iter(self.fields):
      self.fields[field].widget.attrs.update({
        'class': 'form-control',
        'placeholder': None
      })


  def save(self, commit=True, *args, **kwargs):
    sport = super(CreateNewSportForm, self).save(commit=False)
    created_by = kwargs.pop('created_by', None)
    if not created_by:
      raise forms.ValidationError("NO USER ID FOUND")

    sport.created_by = created_by
    if commit:
      sport.save()
    return sport

class CreateNewFacilityForm(forms.ModelForm):
  class Meta:
    model = Facility
    fields = (
      'sport',
      'name',
      'type',
      'location',
      'google_map_link',
      'capacity',
      'inventory',
      'remarks',
      'safety_regulations'
    )

  def __init__(self, *args, **kwargs):
    super(CreateNewFacilityForm, self).__init__(*args, **kwargs)
    for field in iter(self.fields):
      self.fields[field].widget.attrs.update({
        'class': 'form-control',
        'placeholder': None
      })

  def save(self, commit=True, *args, **kwargs):
    facility = super(CreateNewFacilityForm, self).save(commit=False)
    created_by = kwargs.pop('created_by', None)
    if not created_by:
      raise forms.ValidationError("NO USER ID FOUND")

    facility.created_by = created_by
    if commit:
      facility.save()
    return facility

class CreateNewSlotForm(forms.ModelForm):
  class Meta:
    model = Slot
    fields = (
      'sport',
      'facility',
      'duration',
      'timeStart',
      'timeEnd',
      'frequency'
    )

  def __init__(self, *args, **kwargs):
    super(CreateNewSlotForm, self).__init__(*args, **kwargs)
    for field in iter(self.fields):

      self.fields[field].widget.attrs.update({
        'class': 'form-control',
        'placeholder': None
      })

    # self.fields['facility'].queryset = Facility.objects.filter(sport=2)

  def save(self, commit=True, *args, **kwargs):
    slot = super(CreateNewSlotForm, self).save(commit=False)
    created_by = kwargs.pop('created_by', None)
    if not created_by:
      raise forms.ValidationError("NO USER ID FOUND")

    slot.created_by = created_by
    if commit:
      slot.save()
    return slot
