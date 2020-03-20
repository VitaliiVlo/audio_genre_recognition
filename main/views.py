import logging
import os
import tempfile

from django.http import JsonResponse
from django.shortcuts import render

from audio_recognition.simple.main import predict_genre

logger = logging.getLogger(__name__)


def main(request):
    return render(request, 'main.html')


def recognize(request):
    audio = request.FILES.get('audio')
    logger.warning("audio1")
    with tempfile.TemporaryDirectory() as tmpdirname:
        logger.warning(tmpdirname)
        audio_path = os.path.join(tmpdirname, "audio.mp3")
        with open(audio_path, "wb") as f:
            f.write(audio.read())
        logger.warning("audio created")
        genre = predict_genre(audio_path)
        logger.warning("genre predicted")
        return JsonResponse({"genre": genre})
