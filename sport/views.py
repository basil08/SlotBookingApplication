from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import datetime

from .utils import is_staff_member, is_user
from .forms import CreateNewFacilityForm, CreateNewSportForm
from .models import Facility, Sport, SlotBook
from authentication.models import User

@login_required
def dashboard(request):
  return HttpResponse("This is the SPORT DASHBOARD")

@login_required
@user_passes_test(is_staff_member)
def create_new_sport(request):
  if request.method == 'POST':
    form = CreateNewSportForm(request.POST, request.FILES)
    if form.is_valid():
      form.save(created_by=request.user)
      messages.success(request, "Sport saved successfully!")
      return render(request, "sport/new.html")
    else:
      messages.error(request, "Errors in form!")
      return render(request, "sport/new.html", { 'errors': form.errors })
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
@user_passes_test(is_staff_member)
def sports_list(request):
  # get a list of all sports created by all staff
  sports = Sport.objects.all()
  return render(request, 'sport/staffSportsListPage.html', {'sports': sports})

@login_required
@user_passes_test(is_staff_member)
def sport_page(request, sport_id):
  sport = Sport.objects.get(pk=sport_id)
  facilities = Facility.objects.filter(sport=sport)
  bookingCount = len(SlotBook.objects.filter(bookingDate__gte=datetime.date.today(), sport=sport))
  return render(request, 'sport/staffSportPage.html', { 'sport': sport, 'facilities': facilities, 'bookingCount': bookingCount })

@login_required
@user_passes_test(is_staff_member)
def facility_page(request, facility_id):
  facility = Facility.objects.select_related().get(pk=facility_id)
  slotBookings = SlotBook.objects.select_related().filter(facility=facility)
  return render(request, 'sport/facilityPage.html', { 'f': facility, 'slotBookings': slotBookings })

@login_required
@user_passes_test(is_staff_member)
def slot_bookings(request):
  pass

@login_required
@user_passes_test(is_staff_member)
def create_new_facility(request):
  if request.method == 'POST':
    form = CreateNewFacilityForm(request.POST, request.FILES)
    if form.is_valid():
      form.save(created_by=request.user)
      messages.success(request, "Facility saved successfully!")
      return render(request, "sport/createNewFacility.html")
    else:
      messages.error(request, "Errors in form!")
      return render(request, "sport/createNewFacility.html", { 'errors': form.errors })
  else:
    form = CreateNewFacilityForm()

  return render(request, 'sport/createNewFacility.html', { 'form': form })

@login_required
@user_passes_test(is_staff_member)
def create_new_slot(request):
  pass

@login_required
@user_passes_test(is_staff_member)
def update_sport(request):
  pass

@login_required
@user_passes_test(is_staff_member)
def update_facility(request):
  pass

@login_required
@user_passes_test(is_staff_member)
def update_slot(request):
  pass

@login_required
@user_passes_test(is_staff_member)
def cancel_slot_booking(request, slotbook_id):
  try:
    slotBook = SlotBook.objects.get(pk=slotbook_id)
    slotBook.delete()
    messages.success(request, "Slot Booking with id {} was cancelled. The slot is empty now.".format(slotBook.id))
    return redirect('sport:facilityPage')
  except:
    messages.error(request, "Something went wrong! Please try again!")
    return redirect('sport:facilityPage')

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
  pass

@login_required
def booking_history(request, user_id):
  if request.user.level == 300 and request.user.id != user_id:
    messages.error(request, "Access denied!")
    return redirect('sport:dashboard')

  user = User.objects.get(pk=user_id)
  slotBookings = SlotBook.objects.filter(created_by=user, bookingDate__gte=datetime.date.today())
  pastBookings = SlotBook.objects.filter(created_by=user, bookingDate__lte=datetime.date.today())
  return render(request, 'sport/bookingHistory.html', { 'slotBookings': slotBookings, 'pastBookings': pastBookings })


