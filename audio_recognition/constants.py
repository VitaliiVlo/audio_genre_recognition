import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(os.path.dirname(BASE_DIR), 'genres')

RECOGNITION_LENGTH = 10

COL_NAMES = ['genre', 'signal_mean', 'signal_std', 'signal_skew', 'signal_kurtosis',
             'zcr_mean', 'zcr_std', 'rmse_mean', 'rmse_std', 'tempo',
             'spectral_centroid_mean', 'spectral_centroid_std',
             'spectral_bandwidth_2_mean', 'spectral_bandwidth_2_std',
             'spectral_bandwidth_3_mean', 'spectral_bandwidth_3_std',
             'spectral_bandwidth_4_mean', 'spectral_bandwidth_4_std'] + \
            ['spectral_contrast_' + str(i + 1) + '_mean' for i in range(7)] + \
            ['spectral_contrast_' + str(i + 1) + '_std' for i in range(7)] + \
            ['spectral_rolloff_mean', 'spectral_rolloff_std'] + \
            ['mfccs_' + str(i + 1) + '_mean' for i in range(20)] + \
            ['mfccs_' + str(i + 1) + '_std' for i in range(20)] + \
            ['chroma_stft_' + str(i + 1) + '_mean' for i in range(12)] + \
            ['chroma_stft_' + str(i + 1) + '_std' for i in range(12)]
