from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.preprocessing import MinMaxScaler
from scipy.signal import welch, freqz, butter, filtfilt
from io import BytesIO
from PIL import Image
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
import os, time
import matplotlib.pyplot as plt
from scipy.io import loadmat
from collections import Counter
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.preprocessing import MinMaxScaler
from scipy.signal import welch, freqz, butter, filtfilt
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import decimate
from sklearn.preprocessing import StandardScaler

def generate_num():
    # CSV 파일에서 데이터 로드
    df = pd.read_csv('assets/sample_SE.csv', usecols=['Channel_2', 'Channel_3'])
    size = int((df.shape[0]/256)/60)

    # 두 데이터프레임을 concat으로 합치기
    # 여기서는 두 채널을 합쳤지만, 논문의 방법에 따라 적절한 처리가 필요할 수 있습니다.
    # 예를 들어, 논문에서는 AF3 및 AF4 채널을 사용했으므로 해당 채널에 대해 처리해야 할 것입니다.

    # 최종 데이터프레임 확인
    print("DataFrame shape:", df.shape)
    df.head()


    # Channel_2와 Channel_3 데이터 가져오기
    data_channel_2 = df['Channel_2'].values
    data_channel_3 = df['Channel_3'].values

    # 주파수 변환 수행
    def calculate_fft(data, sample_rate):
        n = len(data)
        yf = fft(data)
        xf = fftfreq(n, 1 / sample_rate)
        return xf[:n//2], 2.0/n * np.abs(yf[0:n//2])

    # 시각화를 위해 샘플 주파수 및 성분 계산
    sample_rate = 256
    xf_channel_2, yf_channel_2 = calculate_fft(data_channel_2, sample_rate)
    xf_channel_3, yf_channel_3 = calculate_fft(data_channel_3, sample_rate)

    # Bandpass 필터링을 수행하고 필터링된 주파수 성분 계산
    def bandpass_filter(data, low_freq, high_freq, sample_rate):
        n = len(data)
        yf = fft(data)
        xf = fftfreq(n, 1 / sample_rate)

        # Bandpass 필터링
        yf[(xf < low_freq) | (xf > high_freq)] = 0

        # 역 FFT 수행
        filtered_data = np.real(np.fft.ifft(yf))

        return filtered_data

    # Bandpass 필터 적용
    low_freq = 0.01  # 낮은 주파수 제한
    high_freq = 30  # 높은 주파수 제한
    filtered_channel_2 = bandpass_filter(data_channel_2, low_freq, high_freq, sample_rate)
    filtered_channel_3 = bandpass_filter(data_channel_3, low_freq, high_freq, sample_rate)
    # Stop-pass 필터링
    def stop_pass_filter(data, stop_freq, sample_rate):
        nyquist = 0.5 * sample_rate
        normal_stop = stop_freq / nyquist
        b, a = butter(4, normal_stop, btype='high', analog=False)
        y = filtfilt(b, a, data)
        return y

    # 50/60 Hz powerline noise 제거
    stop_freq = 50  # 논문에서 언급된 값, 필요에 따라 조절 가능
    filtered_channel_2 = stop_pass_filter(filtered_channel_2, stop_freq, sample_rate)
    filtered_channel_3 = stop_pass_filter(filtered_channel_3, stop_freq, sample_rate)

    # Gaussian 스무딩 필터 적용
    def gaussian_smooth(data, window_size):
        return np.convolve(data, np.ones(window_size)/window_size, mode='same')

    window_size = 100
    smoothed_channel_2 = gaussian_smooth(filtered_channel_2, window_size)
    smoothed_channel_3 = gaussian_smooth(filtered_channel_3, window_size)

    # Normalize data using MinMaxScaler
    scaler = MinMaxScaler()
    smoothed_channel_2_normalized = scaler.fit_transform(smoothed_channel_2.reshape(-1, 1)).flatten()
    smoothed_channel_3_normalized = scaler.fit_transform(smoothed_channel_3.reshape(-1, 1)).flatten()

    # Detected Eye Blinks with Threshold (Assuming you have the peaks detected)
    # You may need to adjust the threshold based on your data
    threshold = 0.5  # Adjust the threshold value

    peaks_channel_2_indices, _ = find_peaks(smoothed_channel_2_normalized, height=threshold)
    peaks_channel_3_indices, _ = find_peaks(smoothed_channel_3_normalized, height=threshold)

    # Get the number of peaks
    num_peaks_channel_2 = len(peaks_channel_2_indices)
    num_peaks_channel_3 = len(peaks_channel_3_indices)

    # 두 채널의 블링크 횟수 통합
    integrated_blink_count = num_peaks_channel_2 + num_peaks_channel_3

    return integrated_blink_count//size