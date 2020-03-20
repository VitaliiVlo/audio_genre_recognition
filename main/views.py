import os
import tempfile

from django.http import JsonResponse
from django.shortcuts import render

from audio_recognition.simple.main import predict_genre


def main(request):
    return render(request, 'main.html')


def recognize(request):
    audio = request.FILES.get('audio')
    with tempfile.TemporaryDirectory() as tmpdirname:
        audio_path = os.path.join(tmpdirname, "audio.mp3")
        with open(audio_path, "wb") as f:
            f.write(audio.read())
        genre = predict_genre(audio_path)
        return JsonResponse({"genre": genre})
