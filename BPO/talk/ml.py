import sounddevice as sd
import numpy as np
import wave
import time
import threading
import keyboard
from faster_whisper import WhisperModel
from transformers import pipeline

class WhisperTranscriber:
    def __init__(self, model_size="medium", sample_rate=44100):
        self.sample_rate = sample_rate
        self.model = WhisperModel(
            model_size_or_path=model_size,
            device="cpu",
            compute_type="float32"
        )

    def transcribe(self, audio_path):
        segments, _ = self.model.transcribe(audio_path)
        return " ".join(segment.text for segment in segments)

class AudioRecorder:
    def __init__(self, file_name="recording.wav", sample_rate=44100):
        self.file_name = file_name
        self.sample_rate = sample_rate
        self.recording = False
        self.audio_data = []

    def record_audio(self):
        self.recording = True
        print("Recording started.")
        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype=np.int16, callback=self.audio_callback):
            while self.recording:
                sd.sleep(100)
        print("Recording stopped.")
        self.save_audio()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_data.append(indata.copy())

    def save_audio(self):
        audio_data = np.concatenate(self.audio_data, axis=0)
        with wave.open(self.file_name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

    def stop_recording(self):
        self.recording = False

def monitor_silence(recorder, silence_duration=5):
    silence_start_time = None
    while recorder.recording:
        time.sleep(1)
        if len(recorder.audio_data) > 0:
            last_audio_chunk = recorder.audio_data[-1]
            if np.max(np.abs(last_audio_chunk)) < 0.01:
                if silence_start_time is None:
                    silence_start_time = time.time()
                elif time.time() - silence_start_time > silence_duration:
                    print("Silence detected for {} seconds. Stopping recording.".format(silence_duration))
                    recorder.stop_recording()
                    break
            else:
                silence_start_time = None

def analyze_sentiment(text):
    sentiment_analyzer = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment", framework='pt')
    sentiment = sentiment_analyzer(text)[0]
    return sentiment

def analyze_emotion(text):
    emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
    emotions = emotion_classifier(text)
    filtered_emotions = [emotion for emotion in emotions[0] if emotion['label'] != 'neutral']
    most_probable_emotion = max(filtered_emotions, key=lambda x: x['score']) if filtered_emotions else None
    return most_probable_emotion

if __name__ == "__main__":
    recorder = AudioRecorder(sample_rate=44100)
    transcriber = WhisperTranscriber(model_size="medium")
    recording_thread = threading.Thread(target=recorder.record_audio)
    recording_thread.start()
    silence_monitor_thread = threading.Thread(target=monitor_silence, args=(recorder,))
    silence_monitor_thread.start()
    keyboard.wait('space') 
    recorder.stop_recording()
    recording_thread.join()
    silence_monitor_thread.join()
    audio_file = recorder.file_name
    transcription = transcriber.transcribe(audio_file)
    print("\nTranscription:")
    print(transcription)
    
    sentiment = analyze_sentiment(transcription)
    print ("\nSentiment Analysis:")
    print(sentiment)

    most_probable_emotion = analyze_emotion(transcription)
    if most_probable_emotion:
        print("\nMost Probable Emotion:")
        print(f"{most_probable_emotion['label']}: {most_probable_emotion['score']:.4f}")
    else:
        print("\nNo emotions detected (excluding neutral).")