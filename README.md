# SYNOPSIS   

`SlotBookingApplication` is a slot booking management system to enable staff and admins to create slots for sports facility and allow users to conveniently book slots.   

Features:   
1. Email notification triggers on slot manipulation events.   
2. Access control and authorization to user.  
3. Staff can create sport, facilities for each sport, and multiple slots for each facility. They can cancel with an optional remark.  
4. Users can review for slots they booked after the booking date is past.   

This is part of DevClub recruitment tasks 2022'-23'.   

# RUN THIS PROJECT  

0. Update `sport.models.Sport`, `sport.models.Slot`: make created_by field non-nullable.    
1. Update EMAIL_SETTINGS in settings.py   
  a. Make an .env file with EMAIL_PASSWORD set to app password of 2FA authenticated google SMTP app and EMAIL_HOST_USER set to the sender's valid email id. For more, see https://stackoverflow.com/a/28421995  
2. Update database if you want a different backend (for eg: Postgres, etc.). By default, uses SQLite3  
3. Setup virtual environment
4. Run `pip install -r ./requirements.txt`   
5. Run `python manage.py makemigrations`   
6. Run `python manage.py migrate`    
7. Run `python manage.py runserver`    

This starts a local development server ideal for testing. Optionally create a superuser by `python manage.py createsuperuser` although, SlotBookingApplication provides an endpoint at `/auth/signup`   

# NOTE
1. created_by is nullable in current Sport model. This is only for development convenience. In production, it must be non-nullable

# TODO

1. Make dashboard   
6. Delete resources (sport, facility, slot)   
~2. Update features~    
~3. Email service~    
4. Limit number of slots a user can book per day    
~7. Review and rating system~    
5. Email verification    
6. Streamline slot making process - daily, weekly, monthly, annually, etc.    
2. Limit choices of facilities to selected sport in CreateNewSlotForm    
~3. decide duration: FloatField ok or not since timeStart - timeEnd should match duration in CreateNewSlotForm~
~4. Add a note explaining reason for cancellation in email when staff cancels a booking~

# Email usecases   

~1. When a slot is updated, notify everyone who booked that slot~
~2. Successfully booked a slot~
~3. Booking cancelled by an admin~

# APPLICATION DESIGN

Please see design doc attached as a PDF
