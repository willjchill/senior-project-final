clear;
clc;
clf;

% Sample signal
filename = "contraction_ex.csv";
x = csvread(filename);
x = x - mean(x); % remove DC

% Perform discrete wavelet transform (DWT)
level = 3
coefficients = modwt(x(1:1000), level, 'sym4'); 

figure(1)
for i = 1:level+1
    subplot(level+1,1,i)
    plot(coefficients(i,:))
end

figure(2)
plot(x(1:1000))

filename = "emg_contraction5.csv";
x = csvread(filename);
level = 3;
figure(3)
for i = 1:level+1
    subplot(level+1,1,i)
    plot(x(i,:))
end




% % saving filtered FFT into directory
% currentPath = pwd;
% folder = '\contraction_filtered_v2\';
% raw_folder = '\contractionraw\';
% files = dir(fullfile([pwd,raw_folder], '*.csv'))
% 
% for i = 1:numel(files)
%     filename = fullfile([pwd,raw_folder], files(i).name);
% 
%     % Sample signal
%     x = csvread(filename);
%     x = x - mean(x); % remove DC
%     level = 4;
%     [coefficients, ~] = wavedec(x(1:1000), level, 'db1'); 
%     x = reshape(coefficients(1:1000), [], level);
%     filepath = fullfile([pwd,folder], files(i).name);
%     csvwrite(filepath, x); % writing to filtered
% end