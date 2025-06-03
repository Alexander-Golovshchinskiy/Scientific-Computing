
clear;
clc;
%% Adding Demo Data folder path to MATLAB path
script_folder = fileparts(mfilename('fullpath')); % Script folder
data_folder = fullfile(script_folder, 'Demo data');    % Path to 'Demo data'
addpath(genpath(data_folder));                    % Adds it to the MATLAB path

%% Constants for Demo Data
DEMO_LASER_FILES = {'PurpleLaser.csv', 'RedLaser.csv'};
DEMO_KNOWN_WAVELENGTHS = [405, 650]; 
DEMO_DYE_FILES = {'BlueDye.csv', 'RedDye.csv'};
DEMO_BLANK_FILES = {'BlankForBlue.csv', 'BlankForRed.csv'};
DEMO_WHITE_LED_FILE = 'WhiteLED.csv'; 
SMOOTHING_WINDOW = 100; 
COLORMAP = {'Blue', 'Red', 'Green'};
%% Constants for Our Data
LASER_FILES = {'PurpleLaser05s_AleksandrGolovshchinskii.csv', 'RedLaser05s_AleksandrGolovshchinskii.csv', 'GreenLaser05s_AleksandrGolovshchinskii.csv'};
KNOWN_WAVELENGTHS = [405, 650, 532]; 
DYE_FILES = {'BlueDye2s_AleksandrGolovshchinskii.csv', 'RedDye2s_AleksandrGolovshchinskii.csv'};
BLANK_FILES = {'BlankForBlue2s_AleksandrGolovshchinskii.csv', 'BlankForRed2s_AleksandrGolovshchinskii.csv'};
WHITE_LED_FILE = 'WhiteLED09s_AleksandrGolovshchinskii.csv'; 
%% Run Main Function for Demo Data
disp('Processing Demo Data...');
main(DEMO_LASER_FILES, DEMO_KNOWN_WAVELENGTHS, DEMO_DYE_FILES, DEMO_BLANK_FILES, DEMO_WHITE_LED_FILE, SMOOTHING_WINDOW, COLORMAP, 'Demo Data');

%% Run Main Function for Our Data
disp('Processing Our Data...');
main(LASER_FILES, KNOWN_WAVELENGTHS, DYE_FILES, BLANK_FILES, WHITE_LED_FILE, SMOOTHING_WINDOW, COLORMAP, 'Collected Data');

%% Main Function Definition
function main(laser_files, known_wavelengths, dye_files, blank_files, led_file, smoothing_window, colormap, dataset_name)
    %Calibration
    [m, c, wavelengths_fn] = calibrate_spectrometer(laser_files, known_wavelengths);

    %Wavelength and Absorbance Calculation
    [wavelengths, absorbance] = calculate_absorbance(dye_files, blank_files, wavelengths_fn);

    %Noise Filtering
    cleaned_absorbance = filter_noise(absorbance);

    %Smoothing
    smoothed_absorbance = smooth_spectrum(cleaned_absorbance, smoothing_window);

    %Plotting
    plot_spectra(dye_files, smoothed_absorbance, wavelengths_fn, laser_files, led_file, colormap, dataset_name);

    disp('Successful!')
end


%% Function Definitions

function plot_spectra(dye_files, smoothed_absorbance, wavelengths_fn, laser_files, led_file, colormap, dataset_name)
    % Plot smoothed absorbance spectra of red and blue dyes
    figure;
    for i = 1:length(dye_files)
        % Generate accurate wavelength axis
        wavelengths = wavelengths_fn(1:size(smoothed_absorbance, 1));
        plot(wavelengths, smoothed_absorbance(:, i),lower(colormap{i}(1)), 'DisplayName', [colormap{i}, ' Dye']);
        hold on;
    end
    hold off;
    title(['Smoothed Absorbance Spectra of Dyes - ', dataset_name]);
    xlabel('Wavelength (nm)');
    ylabel('Absorbance');
    legend('show');

    % Plot unsmoothed spectra of the white LED and calibration lasers
    figure;
    % Plot white LED spectrum
    led_spectrum = csvread(led_file);
    led_wavelengths = wavelengths_fn(1:length(led_spectrum));
    plot(led_wavelengths, led_spectrum, 'black', 'DisplayName', 'White LED');
    hold on;

    % Plot calibration lasers
    for i = 1:length(laser_files)
        laser_spectrum = csvread(laser_files{i});
        laser_wavelengths = wavelengths_fn(1:length(laser_spectrum));
        plot(laser_wavelengths, laser_spectrum, lower(colormap{i}(1)), 'DisplayName', [colormap{i},' Laser']);
    end
    hold off;
    title(['Unsmoothed Spectra of White LED and Calibration Lasers - ', dataset_name]);
    xlabel('Wavelength (nm)');
    ylabel('Intensity');
    legend('show', 'Location','best');
end

%Calibration function
function [m, c, wavelengths_fn] = calibrate_spectrometer(laser_files, known_wavelengths)

    pixel_positions = []; 

    % Loop through laser files for calibration
    for i = 1:length(laser_files)
        spectrum = csvread(laser_files{i});
        max_intensity = max(spectrum);
        max_idx = find(spectrum == max_intensity, 1); %first index found
        pixel_positions = [pixel_positions; max_idx];
    end

    % Solve for calibration parameters [m; c]
    X = [pixel_positions, ones(length(pixel_positions), 1)]; % [pixels, 1]
    Y = known_wavelengths'; 
    params = X \ Y; % mldivide in newer matlab versions
    m = params(1); 
    c = params(2); 

    % Define wavelengths_fn as a function handle
    wavelengths_fn = @(pixels) pixels * m + c; 
end

function [wavelengths, absorbance] = calculate_absorbance(dye_files, blank_files, wavelengths_fn)
    absorbance = []; 

    for i = 1:length(dye_files)

        % Read dye and blank spectra
        IDye = csvread(dye_files{i});
        IBlank = csvread(blank_files{i});

        % Prevent division by zero
        IBlank(IBlank == 0) = NaN;

        %Wavelengths from pixels
        wavelengths = wavelengths_fn(1:length(IDye));

        %Absorbance for each dye
        absorbance(:, i) = 1 - (IDye ./ IBlank);
    end
end


function cleaned_absorbance = filter_noise(absorbance)
    cleaned_absorbance = NaN(size(absorbance));

    % Process each column (dye) independently
    for col = 1:size(absorbance, 2)
        % Extract the current dye's absorbance
        data = absorbance(:, col);

        % Calculate moving standard deviation

        moving_std = NaN(size(data));
    
        for i = 2:length(data)
            % Get the current pair of points
            pair = data(i-1:i);
            
            % How drastically values in the pair differ around their mean
            moving_std(i) = std(pair, 'omitnan');
        end

        % Baseline for difference assumed at the centre of the spectrum
        median_value = median(moving_std, 'omitnan');

        % Find noisy regions
        diff_vector = abs(moving_std - median_value); % Substract the baseline
        % Mean difference chosen as a threshold for cutoff
        mean_diff = mean(diff_vector, 'omitnan');
        noisy_mask = moving_std > mean_diff;

        % Remove noisy regions
        cleaned_data = data;
        cleaned_data(noisy_mask) = NaN;

        % Remove additional noisy regions beyond cutoff points
        noisy_indices = find(noisy_mask);
        if ~isempty(noisy_indices)
            left_cutoff = max(noisy_indices(noisy_indices < length(data) / 2));
            right_cutoff = min(noisy_indices(noisy_indices > length(data) / 2));
            cleaned_data(1:left_cutoff) = NaN;
            cleaned_data(right_cutoff:end) = NaN;
        end

        
        cleaned_absorbance(:, col) = cleaned_data;
    end
end


function smoothed_absorbance = smooth_spectrum(absorbance, smoothing_window)
    smoothed_absorbance = NaN(size(absorbance)); 

    % Loop through each column (dye) in absorbance
    for col = 1:size(absorbance, 2)
        data = absorbance(:, col); % Extract column
        for i = 1:length(data)
            % Define window bounds
            start_idx = max(1, i - smoothing_window); % Ensure bounds
            end_idx = min(length(data), i + smoothing_window);
            window = data(start_idx:end_idx); % Extract window

            % Compute mean of the window
            smoothed_absorbance(i, col) = nanmean(window);
        end
    end
end


