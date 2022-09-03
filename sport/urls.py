from django.urls import path, include

from . import views

app_name = "sport"

urlpatterns = [
  # common routes
  path('', views.index, name='index'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('bookingHistory/<int:user_id>/', views.booking_history, name='bookingHistory'),
  # work
  path('profile/', views.profile, name='profile'),
  # work
  path('sportsList/', views.sports_list, name='sportsList'),
  path('sportPage/<int:sport_id>/', views.sport_page, name='sportPage'),
  # staff routes
  path('facilityPage/<int:facility_id>/', views.facility_page, name='facilityPage'),
  path('slotBookings/', views.slot_bookings, name='slotBookings'),
  path('newSport/', views.create_new_sport, name='newSport'),
  path('newFacility/', views.create_new_facility, name='newFacility'),
  path('newSlot/', views.create_new_slot, name='newSlot'),
  path('newReview/', views.create_new_review, name='newReview'),
  path('updateSport/<int:sport_id>/', views.update_sport, name='updateSport'),
  path('updateFacility/<int:facility_id>/', views.update_facility, name='updateFacility'),
  path('updateSlot/<int:slot_id>/', views.update_slot, name='updateSlot'),
  path('cancelSlotBooking/<int:slot_id>/', views.cancel_slot_booking, name="cancelSlotBooking"),
  path('userList/', views.user_list, name="userList"),
  # user routes
  path('bookSlot/<int:slot_id>/', views.book_slot, name='bookSlot')
]