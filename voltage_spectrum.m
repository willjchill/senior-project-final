clear;
clc;
clf;

filename = 'voltageTest.csv';

signal = csvread(filename);

raw_signal = signal;

Ts = 1/1000; % 1ms sampling time
Fs = 1/Ts; 

% Length of the signal
N = length(signal);

% Define the size of the moving window
%window_size = 5;
% Create the moving average filter kernel
%kernel = ones(1, window_size) / window_size;
% Apply the moving average filter using convolution
%signal = conv(signal, kernel, 'valid');
%N = length(signal);

cutoff_frequency = 200; % Cutoff frequency in Hz
normalized_cutoff_frequency = cutoff_frequency / (Fs/2); % Sampling frequency in Hz
order = 4; % Filter order
[b, a] = butter(order, normalized_cutoff_frequency, 'low');
signal = filtfilt(b, a, signal);

% Perform FFT
fft_signal = fft(signal);
fft_signal(1) = 0; % removing DC signal

% Generate frequency axis
f = linspace(-Fs/2, Fs/2, N); % Frequency axis from -Fs/2 to Fs/2
fft_signal_shifted = fftshift(fft_signal);

% Plot the magnitude spectrum
figure(1);
plot(f, fftshift(abs(fft_signal)));
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Filtered Magnitude Spectrum');

figure(2);
plot(1:N, ifft(fft_signal));
title('Filtered EMG Signal');

figure(3)
plot(1:length(raw_signal), raw_signal);
title('Unfiltered EMG Signal');
xlabel('Samples')
ylabel('Voltage from ADC (0-1023)')
xlim([0 length(raw_signal)-1])

% saving filtered FFT into directory
currentPath = pwd;
folder = '\restraw_filtered_v2\';
raw_folder = '\restdataraw\';
files = dir(fullfile([pwd,raw_folder], '*.csv'))

for i = 1:numel(files)
    filename = fullfile([pwd,raw_folder], files(i).name);

    % Read the contents of the file
    signal = csvread(filename);
    signal = filtfilt(b, a, signal); % filter LPF
    signal = fft(signal); % getting frequency content
    signal(1) = 0; % removing DC signal
    signal = abs(signal); % getting magnitude
    signal = signal(1:250); % only getting the first 250Hz of data (LPF!)

    filepath = fullfile([pwd,folder], files(i).name);
    csvwrite(filepath, signal); % writing to filtered
end

