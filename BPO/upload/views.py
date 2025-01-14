from django.shortcuts import render
from django.http import request
import pyrebase
import pandas as pd
from .forms import ExcelUploadForm

config = {
    "apiKey": "AIzaSyCzUWZkMoqVhVkiHVP42VnOVXJDoJwf7PI",
    "authDomain": "bpos-1c1d7.firebaseapp.com",
    "databaseURL": "https://bpos-1c1d7-default-rtdb.firebaseio.com/",
    "projectId": "bpos-1c1d7",
    "storageBucket": "bpos-1c1d7.firebasestorage.app",
    "messagingSenderId": "74977650667",
    "appId": "1:74977650667:web:1ef5812aaae832f291dbae"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()

def uploadExcelSheet(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            # Normalize column names
            df.columns = df.columns.str.strip().str.upper()

            # Convert all NaN to None
            df = df.where(pd.notnull(df), None)

            # Prepare data for batch upload
            data_to_upload = {}
            for index, row in df.iterrows():
                date_key = str(row['DATE']) if 'DATE' in df.columns and row['DATE'] else f"row_{index}"
                data_to_upload[date_key] = {
                    'DATE': int(row['DATE']) if row['DATE'] else None,
                    'TIME': str(row['TIME']) if 'TIME' in df.columns else None,
                    'SCHEDULE': row['SCHEDULE'] if 'SCHEDULE' in df.columns else None,
                    'CUSTOMERNAME': str(row['CUSTOMERNAME']) if 'CUSTOMERNAME' in df.columns else None,
                    'PHONENUMBER': int(row['PHONENUMBER']) if 'PHONENUMBER' in df.columns else None,
                }

            # Debug: Log data size (optional)
            print(f"Uploading {len(data_to_upload)} records...")

            # Batch upload
            db.child('appointments').update(data_to_upload)

            return render(request, 'upload/upload.html', {'form': form, 'message': 'Data uploaded successfully!'})
    else:
        form = ExcelUploadForm()

    return render(request, 'upload/upload.html', {'form': form})
