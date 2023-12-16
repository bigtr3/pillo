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
import matplotlib.font_manager as fm

font_path = "C:\\Windows\\Fonts\\NanumGothicLight.ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font',family=font_name)

# 주파수 변환 수행
def calculate_fft(data, sample_rate):
    n = len(data)
    yf = fft(data)
    xf = fftfreq(n, 1 / sample_rate)
    return xf[:n//2], 2.0/n * np.abs(yf[0:n//2])

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

# 주파수 대역 추출 함수
def extract_frequency_band(data, frequency_range, sample_rate):
    low, high = frequency_range
    n = len(data)
    yf = fft(data)
    xf = fftfreq(n, 1 / sample_rate)

    # 주파수 대역에 해당하는 데이터 추출
    band_data = data[(xf >= low) & (xf <= high)]
    xf_band = xf[(xf >= low) & (xf <= high)]

    return xf_band, band_data

# 시간 변환 함수 추가
def convert_to_minutes(seconds):
        return seconds / 60

# 주파수 범위에 해당하는 데이터 비율 계산 함수
def calculate_band_ratio(data, sample_rate, frequency_range):
    n = len(data)
    yf = fft(data)
    xf = fftfreq(n, 1 / sample_rate)

    # 주파수 범위에 해당하는 인덱스 추출
    indices = np.where((xf >= frequency_range[0]) & (xf <= frequency_range[1]))

    # 주파수 범위의 성분 계산
    selected_amplitudes = np.abs(yf[indices])

    # 주파수 범위의 비율 계산
    total_amplitude = np.sum(np.abs(yf))
    ratio = np.sum(selected_amplitudes) / total_amplitude

    return ratio
    
def generate_rate():
        # CSV 파일에서 데이터 로드
        df = pd.read_csv('assets/sample_SE.csv', usecols=['Channel_2', 'Channel_3'])
        size = int((df.shape[0]/256)/60)
        # Channel_2와 Channel_3 데이터 가져오기
        data_channel_2 = df['Channel_2'].values
        data_channel_3 = df['Channel_3'].values

        # 시각화를 위해 샘플 주파수 및 성분 계산
        sample_rate = 256
        xf_channel_2, yf_channel_2 = calculate_fft(data_channel_2, sample_rate)
        xf_channel_3, yf_channel_3 = calculate_fft(data_channel_3, sample_rate)

        
        # Bandpass 필터 적용
        low_freq = 0.01  # 낮은 주파수 제한
        high_freq = 30  # 높은 주파수 제한
        filtered_channel_2 = bandpass_filter(data_channel_2, low_freq, high_freq, sample_rate)
        filtered_channel_3 = bandpass_filter(data_channel_3, low_freq, high_freq, sample_rate)


        # 정규화
        scaler = StandardScaler()
        normalized_data_channel_2 = scaler.fit_transform(filtered_channel_2.reshape(-1, 1)).flatten()
        normalized_data_channel_3 = scaler.fit_transform(filtered_channel_3.reshape(-1, 1)).flatten()

        # Bandpass 필터 적용된 데이터의 주파수 성분 계산
        xf_filtered_channel_2, yf_filtered_channel_2 = calculate_fft(normalized_data_channel_2, sample_rate)
        xf_filtered_channel_3, yf_filtered_channel_3 = calculate_fft(normalized_data_channel_3, sample_rate)


        # 주파수 대역 정의
        delta_range = (0.5, 3)
        theta_range = (4, 7)
        alpha_range = (8, 12)
        beta_range = (13, 30)
        gamma_range = (31, 50)

        # 채널 2개 합치기
        yf_filtered_total = yf_filtered_channel_2 + yf_filtered_channel_3

        # 구간의 개수
        num_intervals = 8
        interval_size = len(yf_filtered_total) // num_intervals

        # 각 구간의 비율을 저장할 리스트
        alpha_ratios = []

        # 각 구간에 대한 비율 계산
        for i in range(num_intervals):
            start_index = i * interval_size
            end_index = (i + 1) * interval_size
            interval_data = yf_filtered_total[start_index:end_index]

            alpha_ratio = calculate_band_ratio(interval_data, sample_rate, alpha_range)
            alpha_ratios.append(alpha_ratio)
            print(f"구간 {i+1} 알파파 비율: {alpha_ratio:.5f}")


        # 전체 증감율 계산 및 출력
        total_percentage_change = ((alpha_ratios[0] - alpha_ratios[-1]) / alpha_ratios[0]) * 100
        print(f"처음 구간 대비 마지막 구간까지 전체 증감율: {total_percentage_change:.2f}%")
        return int(total_percentage_change)