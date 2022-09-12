from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime, date
from django.core.mail import BadHeaderError, send_mail

from .utils import is_staff_member, is_user
from .forms import CreateNewFacilityForm, CreateNewSlotForm, CreateNewSportForm, CreateNewReviewForm
from .models import Facility, Sport, Slot, Review
from authentication.models import User
from copy import deepcopy
import os


@login_required
def index(request):
  return redirect('sport:dashboard')

@login_required
def dashboard(request):
  return render(request, "sport/dashboard.html")

@login_required
@user_passes_test(is_staff_member)
def create_new_sport(request):
  if request.method == 'POST':
    form = CreateNewSportForm(request.POST, request.FILES)
    if form.is_valid():
      form.save(created_by=request.user)
      messages.success(request, "Sport saved successfully!")
      form = CreateNewSportForm()
      return render(request, "sport/createNewSport.html", {'form': form} )
    else:
      messages.error(request, "Errors in form!")
      return render(request, "sport/createNewSport.html", { 'errors': form.errors })
  else:
    form = CreateNewSportForm()

  return render(request, 'sport/new.html', { 'form': form })

@login_required
@user_passes_test(is_staff_member)
def update_sport(request, sport_id):
  sport = get_object_or_404(Sport, pk=sport_id)
  form = CreateNewSportForm(request.POST or None, request.FILES or None, instance=sport)
  if form.is_valid():
    form.save(created_by=request.user)
    messages.success(request, "{} updated successfully!".format(sport.name))
    return redirect("sport:dashboard")
  return render(request, "sport/update.html", { 'form': form, 'sport_id': sport_id, 'title': sport.name })

@login_required
def sports_list(request):
  # get a list of all sports created by all staff
  sports = Sport.objects.all()
  return render(request, 'sport/staffSportsListPage.html', {'sports': sports})

@login_required
def sport_page(request, sport_id):
  sport = Sport.objects.get(pk=sport_id)
  facilities = Facility.objects.filter(sport=sport)
  bookingCount = len(Slot.objects.filter(date__gte=date.today(), sport=sport))
  return render(request, 'sport/staffSportPage.html', { 'sport': sport, 'facilities': facilities, 'bookingCount': bookingCount })

@login_required
def facility_page(request, facility_id):
  facility = Facility.objects.select_related().get(pk=facility_id)
  if request.user.level < 300:
    slots = Slot.objects.select_related().filter(facility=facility).order_by('-date')
    return render(request, 'sport/facilityPage.html', { 'f': facility, 'slots': slots })
  elif request.user.level == 300:
    # handle user
    slots = Slot.objects.filter(facility=facility).order_by('-date')
    return render(request, "sport/facilityPage.html", { 'f': facility, 'slots': slots })

@login_required
@user_passes_test(is_staff_member)
def slot_bookings(request):
  # admin dashboard to cancel any request
  try:
    slots = Slot.objects.select_related().filter(date__gte=date.today()).order_by('date')
    previousSlots = Slot.objects.select_related().filter(date__lte=date.today())
    for slot in previousSlots:
      if slot.is_reviewed:
        review = Review.objects.get(slot=slot.id)
        slot['review'] = review
    return render(request, "sport/allSlotBookings.html", { 'slots': slots, 'previousSlots': previousSlots})
  except:
    messages.error(request, "Error while fetching list of slots")
    return render(request, "sport/allSlotBookings.html")

@login_required
@user_passes_test(is_user)
def create_new_review(request):
  if request.method == 'POST':
    form = CreateNewReviewForm(request.POST)
    if form.is_valid():
      form.save(created_by=request.user)
      messages.success(request, "Review saved successfully!")
      return redirect('sport:dashboard')
    else:
      messages.error(request, "Errors in form!")
      return render(request, "sport/createNewReview.html", { 'form': form })
  else:
    form = CreateNewReviewForm()

  return render(request, "sport/createNewReview.html", {'form': form})

@login_required
@user_passes_test(is_staff_member)
def create_new_facility(request):
  if request.method == 'POST':
    form = CreateNewFacilityForm(request.POST, request.FILES)
    if form.is_valid():
      form.save(created_by=request.user)
      messages.success(request, "Facility saved successfully!")
      form = CreateNewFacilityForm()
      return render(request, "sport/createNewFacility.html", { 'form': form })
    else:
      messages.error(request, "Errors in form!")
      return render(request, "sport/createNewFacility.html", { 'errors': form.errors })
  else:
    form = CreateNewFacilityForm()

  return render(request, 'sport/createNewFacility.html', { 'form': form })

@login_required
@user_passes_test(is_staff_member)
def create_new_slot(request):
  if request.method == 'POST':
    form = CreateNewSlotForm(request.POST)
    if form.is_valid():
      # this line, omg
      time_diff = (datetime.combine(date.min, form.cleaned_data['timeEnd']) - datetime.combine(date.min, form.cleaned_data['timeStart'])).total_seconds() / 60.0
      if time_diff != float(form.cleaned_data['duration']):
        messages.error(request, 'Inconsistent start and end times. Duration doesn\'t match TimeStart and TimeEnd')
        return render(request, 'sport/createNewSlot.html', {'form': form })
      form.save(created_by=request.user)
      messages.success(request, "Slot saved successfully!")
      form = CreateNewSlotForm()
      return render(request, "sport/createNewSlot.html", { 'form': form})
    else:
      print(form.errors)
      messages.error(request, "Errors in form!")
      return render(request, "sport/createNewSlot.html", { 'errors': form.errors })
  else:
    form = CreateNewSlotForm()

  return render(request, 'sport/createNewSlot.html', { 'form': form })

@login_required
@user_passes_test(is_staff_member)
def update_sport(request, sport_id):
  sport = get_object_or_404(Sport, pk=sport_id)
  form = CreateNewSportForm(request.POST or None, instance=sport)
  if form.is_valid():
    form.save(created_by=request.user)
    messages.success(request, "{} updated successfully!".format(sport.name))
    return redirect("sport:dashboard")
  return render(request, "sport/updateSport.html", { 'form': form, 'sport': sport })

@login_required
@user_passes_test(is_staff_member)
def update_facility(request, facility_id):
  facility = get_object_or_404(Facility, pk=facility_id)
  form = CreateNewFacilityForm(request.POST or None, request.FILES or None, instance=facility)
  if form.is_valid():
    form.save(created_by=request.user)
    messages.success(request, "{} updated successfully!".format(facility.name))
    return redirect("sport:dashboard")
  return render(request, "sport/updateFacility.html", { 'form': form, 'facility': facility })

@login_required
@user_passes_test(is_staff_member)
def update_slot(request, slot_id):
  slot = Slot.objects.select_related().get(pk=slot_id)
  old_slot = deepcopy(slot)
  form = CreateNewSlotForm(request.POST or None, request.FILES or None, instance=slot)
  if form.is_valid():
    time_diff = (datetime.combine(date.min, form.cleaned_data['timeEnd']) - datetime.combine(date.min, form.cleaned_data['timeStart'])).total_seconds() / 60.0
    if time_diff != float(form.cleaned_data['duration']):
      messages.error(request, 'Inconsistent start and end times. Duration doesn\'t match TimeStart and TimeEnd')
      return render(request, 'sport/updateSlot.html', {'form': form, 'slot': slot })
    form.save(created_by=request.user)
    slot = Slot.objects.select_related().get(pk=slot_id)

    if old_slot.is_booked:
      try:
        user = old_slot.booked_by
        send_mail(
          'Slot DETAILS UPDATED: IITD SlotBookingApplication',
          'Dear {},\nThe details of your slot with the following details has been updated:\n{} ({}): {}-{} for {} mins.\n\nThe new details are:\n{} ({}): {}-{} for {} mins.\n\nPlease note the new details. Sorry for the inconvenience.\n\nFor any query, contact {}\n\nBest,\nTechnical Team,\nIITD SlotBookingApplication'
            .format(user.first_name + ' ' + user.last_name, old_slot.facility.name, old_slot.sport.name, old_slot.timeStart, old_slot.timeEnd, old_slot.duration, slot.facility.name, slot.sport.name, slot.timeStart, slot.timeEnd, slot.duration, slot.sport.POCEmail),
          os.getenv('EMAIL_HOST_USER'),
          [user.email],
          fail_silently=False
        )
      except BadHeaderError:
        messages.error(request, 'Slot Updated! Couldn\'t send email. Please contact admin for acknowledgement')
        return redirect('sport:facilityPage', facility_id=slot.facility.id)
      except:
        messages.error(request, "Something went wrong while sending email. Please contact admin for acknowledgement")
        return redirect('sport:facilityPage', facility_id=slot.facility.id)

    messages.success(request, "{} updated successfully! If this slot was booked, the booker is notified by email.".format(slot.sport.name))
    return redirect("sport:dashboard")
  return render(request, "sport/updateSlot.html", { 'form': form, 'slot': slot })

@login_required
@user_passes_test(is_staff_member)
def cancel_slot_booking(request, slot_id):
  if request.method == 'POST':
    remark = request.POST.get('remark', None)
    try:
      slot = Slot.objects.select_related().get(pk=slot_id)
      slot.is_booked = False
      user = slot.booked_by
      slot.booked_by = None
      slot.save()

      if remark:
        remark_text = 'Reason for cancellation: {}.'.format(remark)
      else:
        remark_text = 'No reason for cancellation given. You may contact sport POC.'
      try:
        send_mail(
          'Slot booking CANCELLATION: IITD SlotBookingApplication',
          'Dear {},\nYour slot with the following details:\n{} ({}): {}-{} for {} mins stands cancelled.\n\n{}\n\nSorry for the inconvenience.\n\nFor any query, contact {}\n\nBest,\nTechnical Team,\nIITD SlotBookingApplication'
            .format(user.first_name + ' ' + user.last_name, slot.facility.name, slot.sport.name, slot.timeStart, slot.timeEnd, slot.duration, remark_text, slot.sport.POCEmail),
          os.getenv("EMAIL_HOST_USER"),
          [request.user.email],
          fail_silently=False
        )
      except BadHeaderError:
        messages.error(request, 'Slot Cancelled! Couldn\'t send email. Please contact admin for acknowledgement')
        return redirect('sport:facilityPage', facility_id=slot.facility.id)
      except:
        messages.error(request, "Something went wrong while sending email. Please contact admin for acknowledgement")
        return redirect('sport:facilityPage', facility_id=slot.facility.id)

      messages.success(request, "Slot Booking with id {} was cancelled. The slot is empty now. The Email is sent to the booker!".format(slot.id))
      return redirect('sport:facilityPage', facility_id=slot.facility.id)
    except:
      messages.error(request, "Something went wrong! Please try again!")
      return redirect('sport:facilityPage', facility_id=slot.facility.id)

@login_required
@user_passes_test(is_staff_member)
def user_list(request):
  try:
    users = User.objects.filter(level=300)
    return render(request, 'sport/userList.html', {'users': users})
  except:
    messages.error(request, "Something went wrong! Please try again!")
    return render(request, "sport/userList.html")

#
# USER CENTRIC ROUTES
#

@login_required
def profile(request):
  user =  User.objects.get(pk=request.user.id)
  return render(request, "sport/profile.html", { 'user': user })

# @login_required
# def change_password(request):
#   if request.method == 'POST':
#     form = ChangePasswordForm(request.POST)
#     if form.is_valid():

#       form.save()
#       messages.success(request, "Password changed successfully!")
#       return render(request, "sport/changePassword.html")
#     else:
#       messages.error(request, "Errors in form!")
#       return render(request, "sport/changePassword.html", { 'errors': form.errors })
#   else:
#     form = CreateNewFacilityForm()

#   return render(request, 'sport/createNewFacility.html', { 'form': form })


@login_required
def booking_history(request, user_id):
  if request.user.level == 300 and request.user.id != user_id:
    messages.error(request, "Access denied!")
    return redirect('sport:dashboard')

  user = User.objects.get(pk=user_id)
  slotBookings = Slot.objects.filter(booked_by=user, date__gte=date.today())
  pastBookings = Slot.objects.filter(booked_by=user, date__lte=date.today())
  return render(request, 'sport/bookingHistory.html', { 'user': user, 'slotBookings': slotBookings, 'pastBookings': pastBookings })

@login_required
def book_slot(request, slot_id):
  try:
    slot = Slot.objects.select_related().get(pk=slot_id)
    slot.is_booked = True
    slot.booked_by = request.user
    slot.save()

    try:
      send_mail(
        'Slot booking ACKNOWLEDGEMENT: IITD SlotBookingApplication',
        'Dear {},\n You have successfully booked a slot at {} ({}): {}-{} for {} mins.\n\nPlease follow regulations as specified on the portal. Wishing you a successful event!\n\nFor any query, contact {}\n\nBest,\nTechnical Team,\nIITD SlotBookingApplication'.format(request.user.first_name + ' ' + request.user.last_name, slot.facility.name, slot.sport.name, slot.timeStart, slot.timeEnd, slot.duration, slot.sport.POCEmail),
        os.getenv('EMAIL_HOST_USER'),
        [request.user.email],
        fail_silently=False
      )
    except BadHeaderError:
      messages.error(request, 'Slot Booked! Couldn\'t send email. Please contact admin for acknowledgement')
      return redirect('sport:facilityPage', facility_id=slot.facility.id)
    except:
      messages.error(request, "Something went wrong while sending email. Please contact admin for acknowledgement")
      return redirect('sport:facilityPage', facility_id=slot.facility.id)

    messages.success(request, "You have booked a slot {}: {}-{} for {} mins. Check your inbox for confirmation email.".format(slot.facility.name, slot.timeStart, slot.timeEnd, slot.duration))
    return redirect('sport:facilityPage', facility_id=slot.facility.id)
  except:
    messages.error(request, "Error while booking your slot!")
    return render(request, "sport/facilityPage.html")