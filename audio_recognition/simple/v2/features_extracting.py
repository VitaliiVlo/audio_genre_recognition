import os

import librosa
import numpy as np
import pandas as pd
import scipy.stats
from tqdm import tqdm

from audio_recognition.constants import AUDIO_PATH, COL_NAMES, RECOGNITION_LENGTH


def get_features(y, sr):
    feature_list = list()

    # statistical moments
    feature_list.append(np.mean(abs(y)))
    feature_list.append(np.std(y))
    feature_list.append(scipy.stats.skew(abs(y)))
    feature_list.append(scipy.stats.kurtosis(y))

    # zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y + 0.0001, frame_length=2048, hop_length=512)[0]
    feature_list.append(np.mean(zcr))
    feature_list.append(np.std(zcr))

    # Root Mean Squared Energy
    rmse = librosa.feature.rms(y + 0.0001)[0]  # constant to remove some noise
    feature_list.append(np.mean(rmse))
    feature_list.append(np.std(rmse))

    tempo = librosa.beat.tempo(y, sr=sr)
    feature_list.extend(tempo)

    spectral_centroids = librosa.feature.spectral_centroid(y + 0.01, sr=sr)[0]
    feature_list.append(np.mean(spectral_centroids))
    feature_list.append(np.std(spectral_centroids))

    spectral_bandwidth_2 = librosa.feature.spectral_bandwidth(y + 0.01, sr=sr, p=2)[0]
    spectral_bandwidth_3 = librosa.feature.spectral_bandwidth(y + 0.01, sr=sr, p=3)[0]
    spectral_bandwidth_4 = librosa.feature.spectral_bandwidth(y + 0.01, sr=sr, p=4)[0]
    feature_list.append(np.mean(spectral_bandwidth_2))
    feature_list.append(np.std(spectral_bandwidth_2))
    feature_list.append(np.mean(spectral_bandwidth_3))
    feature_list.append(np.std(spectral_bandwidth_3))
    feature_list.append(np.mean(spectral_bandwidth_4))
    feature_list.append(np.std(spectral_bandwidth_4))

    spectral_contrast = librosa.feature.spectral_contrast(y, sr=sr, n_bands=6, fmin=200.0)
    feature_list.extend(np.mean(spectral_contrast, axis=1))
    feature_list.extend(np.std(spectral_contrast, axis=1))

    spectral_rolloff = librosa.feature.spectral_rolloff(y + 0.01, sr=sr, roll_percent=0.85)[0]
    feature_list.append(np.mean(spectral_rolloff))
    feature_list.append(np.std(spectral_rolloff))

    mfccs = librosa.feature.mfcc(y, sr=sr, n_mfcc=20)
    feature_list.extend(np.mean(mfccs, axis=1))
    feature_list.extend(np.std(mfccs, axis=1))

    chroma_stft = librosa.feature.chroma_stft(y, sr=sr, hop_length=1024)
    feature_list.extend(np.mean(chroma_stft, axis=1))
    feature_list.extend(np.std(chroma_stft, axis=1))

    feature_list = np.round(feature_list, decimals=3).tolist()
    return feature_list


def main():
    df = pd.DataFrame(columns=COL_NAMES)
    genres = os.listdir(AUDIO_PATH)
    for g in tqdm(genres):
        for filename in tqdm(os.listdir(os.path.join(AUDIO_PATH, g))):
            for part in range(30//RECOGNITION_LENGTH):
                file_path = os.path.join(AUDIO_PATH, g, filename)
                y, sr = librosa.load(file_path, mono=True,
                                     duration=RECOGNITION_LENGTH,
                                     offset=part * RECOGNITION_LENGTH)
                feature_list = get_features(y, sr)
                feature_list = [g] + feature_list
                df = df.append(pd.DataFrame(feature_list, index=COL_NAMES).transpose(), ignore_index=True)
    df.to_csv('df_features2_test.csv', index=False)


if __name__ == '__main__':
    main()
