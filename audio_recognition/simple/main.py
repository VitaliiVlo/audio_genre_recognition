import logging
import os
from collections import Counter

import librosa
import numpy as np
from keras.models import load_model
from sklearn.externals import joblib

from audio_recognition.constants import BASE_DIR, RECOGNITION_LENGTH, MAX_AUDIO_DURATION
from audio_recognition.simple.v2.features_extracting import get_features

logger = logging.getLogger(__name__)

path_to_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(path_to_dir, 'model.h5')
std_scale_path = os.path.join(path_to_dir, 'scale.save')
encoder_path = os.path.join(path_to_dir, 'encoder.save')

model = load_model(model_path)
std_scale = joblib.load(std_scale_path)
encoder = joblib.load(encoder_path)


def predict_genre_part(y, sr):
    features = get_features(y, sr)
    features = np.array(features).reshape([1, -1])
    features = std_scale.transform(features)
    predicted_class = model.predict_classes(features)
    return encoder.inverse_transform(predicted_class)[0]


def predict_genre(file_path):
    y, sr = librosa.load(file_path, mono=True, sr=22050, duration=MAX_AUDIO_DURATION)
    length = librosa.get_duration(y, sr=sr)
    predicted_genres = list()
    part_count = int(length // RECOGNITION_LENGTH)
    for part in range(part_count):
        start_idx = part * RECOGNITION_LENGTH * sr
        end_idx = start_idx + RECOGNITION_LENGTH * sr
        y_partial = y[start_idx:end_idx]
        predicted_genre = predict_genre_part(y_partial, sr)
        predicted_genres.append(predicted_genre)
        logger.warning("part" + ", " + "part_count")
    c = Counter(predicted_genres)
    print(c)
    audio_genres = list()
    for key, value in c.items():
        if value >= round(part_count / 3):
            audio_genres.append(key)

    return ", ".join(audio_genres) or 'I dont know'


def main():
    file_path = os.path.join(BASE_DIR, 'simple', 'tracks', 'blues.mp3')
    print(predict_genre(file_path))


if __name__ == '__main__':
    main()
