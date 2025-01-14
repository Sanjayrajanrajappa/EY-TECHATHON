from django.shortcuts import render
from django.http import request
import pyrebase
config = {
  "apiKey": "AIzaSyCzUWZkMoqVhVkiHVP42VnOVXJDoJwf7PI",
  "authDomain": "bpos-1c1d7.firebaseapp.com",
  "databaseURL":"https://bpos-1c1d7-default-rtdb.firebaseio.com/",
  "projectId": "bpos-1c1d7",
  "storageBucket": "bpos-1c1d7.firebasestorage.app",
  "messagingSenderId": "74977650667",
  "appId": "1:74977650667:web:1ef5812aaae832f291dbae"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()

def complaintsViewer(request):
    # Fetch all appointments
    appointments = db.child('appointments').get().val()

    # Check if data exists
    if not appointments:
        return render(request, 'complaints/complaints.html', {'complaints': []})

    # Check if appointments is a list or dictionary
    if isinstance(appointments, list):
        # Filter list of dictionaries
        busy_appointments = [
            appointment for appointment in appointments
            if appointment and appointment.get('SCHEDULE') == 'BUSY'
        ]
    elif isinstance(appointments, dict):
        busy_appointments = [
            appointment for appointment in appointments.values()
            if appointment.get('SCHEDULE') == 'BUSY'
        ]
    else:
        busy_appointments = []
    print("Filtered BUSY appointments:", busy_appointments)
    return render(request, 'complaints/complaints.html', {'complaints': busy_appointments})
