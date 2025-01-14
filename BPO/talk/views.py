import os
import torch
import soundfile as sf
from django.http import JsonResponse
from django.shortcuts import render
from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
import pyrebase

# Firebase configuration
config = {
    "apiKey": "AIzaSyCzUWZkMoqVhVkiHVP42VnOVXJDoJwf7PI",
    "authDomain": "bpos-1c1d7.firebaseapp.com",
    "databaseURL": "https://bpos-1c1d7-default-rtdb.firebaseio.com/",
    "projectId": "bpos-1c1d7",
    "storageBucket": "bpos-1c1d7.firebasestorage.app",
    "messagingSenderId": "74977650667",
    "appId": "1:74977650667:web:1ef5812aaae832f291dbae"
}

# Initialize Firebase with the provided config
firebase = pyrebase.initialize_app(config)

# Get a reference to the Realtime Database
db = firebase.database()
model_name = "openai/whisper-small.en"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

def talker_file(request):
    return render(request, 'talk/talk.html')