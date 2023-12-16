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
    
def generate_plot():
        # CSV 파일에서 데이터 로드
        df = pd.read_csv('assets/sample_SE.csv', usecols=['Channel_2', 'Channel_3'])
        size = int((df.shape[0]/256)/60)
        # Channel_2와 Channel_3 데이터 가져오기
        data_channel_2 = df['Channel_2'].values
        data_channel_3 = df['Channel_3'].values

        # 시각화를 위해 샘플 주파수 및 성분 계산
        sample_rate = 256
        #     xf_channel_2, yf_channel_2 = calculate_fft(data_channel_2, sample_rate)
        #     xf_channel_3, yf_channel_3 = calculate_fft(data_channel_3, sample_rate)

        

        # Bandpass 필터 적용
        low_freq = 0.01  # 낮은 주파수 제한
        high_freq = 30  # 높은 주파수 제한
        filtered_channel_2 = bandpass_filter(data_channel_2, low_freq, high_freq, sample_rate)
        filtered_channel_3 = bandpass_filter(data_channel_3, low_freq, high_freq, sample_rate)

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
        alpha_range = (8, 13)
        beta_range = (14, 26)
        gamma_range = (30, 50)

        # 다운샘플링할 샘플 주기
        downsample_rate = 2  # 예시로 2배 다운샘플링

        # 다운샘플링된 데이터 생성
        downsampled_data_channel_2 = decimate(filtered_channel_2, downsample_rate)
        downsampled_data_channel_3 = decimate(filtered_channel_3, downsample_rate)

        # 정규화
        scaler = StandardScaler()
        normalized_data_channel_2 = scaler.fit_transform(downsampled_data_channel_2.reshape(-1, 1)).flatten()
        normalized_data_channel_3 = scaler.fit_transform(downsampled_data_channel_3.reshape(-1, 1)).flatten()

        # 다운샘플링된 데이터의 주파수 성분 계산
        xf_downsampled_channel_2, yf_downsampled_channel_2 = calculate_fft(normalized_data_channel_2, sample_rate / downsample_rate)
        xf_downsampled_channel_3, yf_downsampled_channel_3 = calculate_fft(normalized_data_channel_3, sample_rate / downsample_rate)

        # 채널 2개 합치기
        yf_filtered_total = yf_filtered_channel_2 + yf_filtered_channel_3


        # 주파수 대역 데이터셋 생성
        delta_xf_channel_total, delta_data_channel_total = extract_frequency_band(yf_filtered_total, delta_range, sample_rate)
        theta_xf_channel_total, theta_data_channel_total = extract_frequency_band(yf_filtered_total, theta_range, sample_rate)
        alpha_xf_channel_total, alpha_data_channel_total = extract_frequency_band(yf_filtered_total, alpha_range, sample_rate)
        beta_xf_channel_total, beta_data_channel_total = extract_frequency_band(yf_filtered_total, beta_range, sample_rate)
        gamma_xf_channel_total, gamma_data_channel_total = extract_frequency_band(yf_filtered_total, gamma_range, sample_rate)

        # 각 주파수 범위에 대한 비율 계산
        delta_ratio_channel_total = calculate_band_ratio(yf_filtered_total, sample_rate, delta_range)
        theta_ratio_channel_total = calculate_band_ratio(yf_filtered_total, sample_rate, theta_range)
        alpha_ratio_channel_total = calculate_band_ratio(yf_filtered_total, sample_rate, alpha_range)
        beta_ratio_channel_total = calculate_band_ratio(yf_filtered_total, sample_rate, beta_range)
        gamma_ratio_channel_total = calculate_band_ratio(yf_filtered_total, sample_rate, gamma_range)

        labels = ['Theta', 'Alpha', 'Beta', 'Gamma']
        ratios = [theta_ratio_channel_total, alpha_ratio_channel_total, beta_ratio_channel_total, gamma_ratio_channel_total]
        colors = ['skyblue', 'lightcoral', 'lightgreen', 'gold']

        fig, ax = plt.subplots(figsize=(8, 8))
        pie = ax.pie(ratios, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)

        # 차트의 위치를 조절합니다.
        ax.set_aspect('equal')  # 원형을 유지하기 위해 가로세로 비율을 동일하게 설정합니다.

        plt.subplots_adjust(top=0.90)
        # 라벨의 글자 크기를 조절합니다.
        ax.set_title('뇌파 종류별 비율', fontsize=28, fontweight="bold", pad=20)
        for text in ax.texts:
                text.set_fontsize(18)
                
        contents = ["졸린 상태에서 나타나는 뇌파","편안한 상태에서 나타나는 뇌파","정신활동(불안, 긴장, 학습)과 관련된 뇌파", '활발한 정신활동(각성,흥분,집중)과 관련된 뇌파']
        # legend를 오른쪽 아래에 위치시킵니다.
        ax.legend(pie[0], contents, loc='lower right', bbox_to_anchor=(1.12, -0.14), fontsize=14)

        # 이미지를 바이트로 변환
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        plt.close()

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


        # 각 구간의 시작 시간 계산
        interval_start_times = [i * (interval_size / sample_rate / 60) for i in range(num_intervals)]

        
        # 피로도 그래프 - y축 대칭 반전
        # 경향성을 꺾은선 그래프로 나타내는 코드
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(interval_start_times, alpha_ratios, marker='o', color='lightgreen', label = '이전 구간 대비 증감 수치')
        plt.subplots_adjust(top=0.83, bottom = 0.14)
        ax.set_title('시간별 피로도 변화', fontsize=28, fontweight='bold', pad=25)
        ax.set_xlabel('시간 (분)', fontsize=18)
        ax.set_ylabel('피로도', fontsize=18)
        ax.set_xticklabels([0, 0, 5,10,15,20], fontsize=14)
        ax.legend(loc = 'lower right',fontsize=14)

        # 각 구간별로 이전 구간 대비 감소율 계산 및 표시
        for i in range(1, num_intervals):
                decrease_percentage = ((alpha_ratios[i-1] - alpha_ratios[i]) / alpha_ratios[i-1]) * 100
                sign = '+' if decrease_percentage >= 0 else '-'
                bbox_props = dict(boxstyle="round,pad=0.25", edgecolor="black", facecolor="white", alpha=0.5, linewidth = 0.5)
                plt.text(interval_start_times[i], alpha_ratios[i], f'{sign}{abs(decrease_percentage):.2f}%', ha='center', va='bottom', fontsize=14, bbox=bbox_props)

        plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        # x축을 기준으로 상하 반전
        plt.gca().invert_yaxis()
        
        # 이미지를 바이트로 변환
        img_buf2 = BytesIO()
        plt.savefig(img_buf2, format='png')
        img_buf2.seek(0)
        plt.close()

        img_1 = Image.open(img_buf)
        img_2 = Image.open(img_buf2)

        result_img = Image.new('RGBA', (img_1.width, img_1.height + img_2.height + 100),(0,0,0,0))  # 추가: 공백 크기를 20으로 설정
        result_img.paste(img_1, (0, 0))
        result_img.paste(img_2, (0, img_1.height + 100), mask=img_2)  # 수정: img_1.height + 20로 변경

        # 합쳐진 이미지를 바이트로 변환
        img_buf_combined = BytesIO()
        result_img.save(img_buf_combined, format='png')
        img_buf_combined.seek(0)

        return img_buf_combined