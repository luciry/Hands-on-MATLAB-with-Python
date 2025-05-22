function result = animation(animation_type, num_frames)
    % ANIMATION Creates animations with MATLAB
    %   result = ANIMATION(animation_type, num_frames)
    %
    %   Parameters:
    %     animation_type - Type of animation ('pendulum', 'wave', 'orbit')
    %     num_frames - Number of frames to generate
    
    % Set default parameters if not provided
    if nargin < 1, animation_type = 'pendulum'; end
    if ~ischar(animation_type), animation_type = 'pendulum'; end
    if nargin < 2, num_frames = 20; end
    num_frames = min(max(num_frames, 10), 50); % Limit frames between 10 and 50
    
    % Debug information
    fprintf('Animation starting: type=%s, frames=%d\n', animation_type, num_frames);
    
    % Ensure output directory exists for frames
    % First, figure out the Flask static directory relative to the Examples/matlab directory
    current_script_dir = fileparts(mfilename('fullpath'));
    project_root = fileparts(fileparts(current_script_dir)); % Go up two levels from Examples/matlab
    static_dir = fullfile(project_root, 'webapp', 'static', 'animation');
    
    fprintf('Using static directory: %s\n', static_dir);
    if ~exist(static_dir, 'dir')
        mkdir(static_dir);
        fprintf('Created static directory\n');
    end
    
    % Clean any existing files
    delete(fullfile(static_dir, '*.png'));
    fprintf('Cleaned existing files\n');
    
    % List to store frame filenames
    frames = cell(1, num_frames);
    fprintf('Allocated %d frame slots\n', num_frames);
    
    % Common figure settings
    fig = figure('Visible', 'off', 'Color', 'white');
    fprintf('Created figure\n');
    
    % Process the animation frames
    fprintf('Starting animation generation: %s\n', animation_type);
    
    switch lower(animation_type)
        case 'pendulum'
            % Simple pendulum animation
            L = 1;  % Length of pendulum (m)
            g = 9.81;  % Gravity (m/s^2)
            theta0 = pi/4;  % Initial angle (rad)
            
            % Time settings
            tmax = 4;  % Maximum time (s)
            dt = tmax/num_frames;  % Time step
            
            % Solve pendulum equation
            pendulum_ode = @(t, y) [y(2); -(g/L)*sin(y(1))];
            [t, y] = ode45(pendulum_ode, linspace(0, tmax, num_frames*10), [theta0; 0]);
            
            % Set up the figure
            set(fig, 'Position', [100, 100, 800, 600]);
            
            % Define consistent axis limits
            axisLimits = [-1.2, 1.2, -1.2, 1.2];
            
            % Generate and save each frame
            for i = 1:num_frames
                clf;
                
                % Get current time
                current_time = (i-1) * dt;
                
                % Find the closest time in our solution
                [~, idx] = min(abs(t - current_time));
                if idx > size(y, 1)
                    idx = size(y, 1);
                end
                current_theta = y(idx, 1);
                
                % Calculate pendulum position
                x = L * sin(current_theta);
                y_pos = -L * cos(current_theta);
                
                % Plot the pendulum
                % Draw the pivot point
                plot(0, 0, 'ko', 'MarkerSize', 10, 'MarkerFaceColor', 'k');
                hold on;
                % Draw the rod
                plot([0, x], [0, y_pos], 'k-', 'LineWidth', 2);
                % Draw the bob
                plot(x, y_pos, 'ro', 'MarkerSize', 15, 'MarkerFaceColor', 'r');
                
                % Configure the plot with fixed axis
                axis equal;
                axis(axisLimits);
                title(sprintf('Pendulum Simulation (t = %.2f s)', current_time));
                grid on;
                
                % Add timestamp
                text(-1.1, -1.1, sprintf('Frame %d/%d', i, num_frames), 'FontSize', 10);
                
                % Save the frame
                frame_filename = fullfile(static_dir, sprintf('frame_%03d.png', i));
                frames{i} = frame_filename;
                print(fig, frame_filename, '-dpng', '-r100');
            end
            
            % Create a summary plot for the thumbnail
            clf;
            % Create a time series of pendulum positions
            sample_times = linspace(0, tmax, 8);
            % Find closest indices
            sample_indices = zeros(1, length(sample_times));
            for j = 1:length(sample_times)
                [~, sample_indices(j)] = min(abs(t - sample_times(j)));
                if sample_indices(j) > size(y, 1)
                    sample_indices(j) = size(y, 1);
                end
            end
            
            % Plot the pendulum path
            plot(0, 0, 'ko', 'MarkerSize', 10, 'MarkerFaceColor', 'k');
            hold on;
            
            for j = 1:length(sample_indices)
                idx = sample_indices(j);
                current_theta = y(idx, 1);
                x = L * sin(current_theta);
                y_pos = -L * cos(current_theta);
                
                % Draw the rod with decreasing opacity (simulated by lighter color)
                fade_factor = 1 - (j-1)/length(sample_indices)*0.7;
                plot([0, x], [0, y_pos], 'k-', 'LineWidth', 2, 'Color', [fade_factor, fade_factor, fade_factor]);
                
                % Draw the bob with decreasing opacity (simulated by lighter red)
                % Remove alpha channel, use lighter red for older positions
                red_color = [1, 1-fade_factor, 1-fade_factor]; % From red to white
                plot(x, y_pos, 'ro', 'MarkerSize', 15, 'MarkerFaceColor', red_color);
            end
            
            % Configure the plot with same fixed axis
            axis equal;
            axis(axisLimits);
            title('Pendulum Motion Over Time');
            grid on;
            
            result.title = 'Pendulum Animation';
            result.description = sprintf('Simple pendulum with length %.1f m starting at angle %.1f rad', L, theta0);
            
        case 'wave'
            % Wave propagation animation
            % Parameters
            amplitude = 1;
            wavelength = 2;
            period = 1;
            
            % Set up the figure
            set(fig, 'Position', [100, 100, 800, 400]);
            
            % Space and time settings
            x = linspace(0, 10, 200);
            tmax = 2;  % Maximum time (s)
            dt = tmax/num_frames;  % Time step
            
            % Define consistent axis limits
            standingWaveAxis = [0, 10, -1.2, 1.2];
            travelingWaveAxis = [0, 10, -1.2, 1.2];
            
            % Generate and save each frame
            for i = 1:num_frames
                clf;
                
                % Current time
                t = (i-1) * dt;
                
                % Calculate wave at current time
                k = 2*pi/wavelength;  % Wave number
                omega = 2*pi/period;  % Angular frequency
                
                % Standing wave
                y1 = amplitude * sin(k*x) * cos(omega*t);
                
                % Traveling wave
                y2 = amplitude * sin(k*x - omega*t);
                
                % Plot the waves
                subplot(2,1,1);
                plot(x, y1, 'b-', 'LineWidth', 2);
                axis(standingWaveAxis);
                title(sprintf('Standing Wave (t = %.2f s)', t));
                grid on;
                ylabel('Amplitude');
                
                subplot(2,1,2);
                plot(x, y2, 'r-', 'LineWidth', 2);
                axis(travelingWaveAxis);
                title(sprintf('Traveling Wave (t = %.2f s)', t));
                grid on;
                xlabel('Position (x)');
                ylabel('Amplitude');
                
                % Save the frame
                frame_filename = fullfile(static_dir, sprintf('frame_%03d.png', i));
                frames{i} = frame_filename;
                print(fig, frame_filename, '-dpng', '-r100');
            end
            
            % Create a summary plot for the thumbnail
            clf;
            
            % Show the wave at different times
            sample_times = linspace(0, tmax, 4);
            colors = winter(length(sample_times));
            
            subplot(2,1,1);
            hold on;
            for j = 1:length(sample_times)
                t = sample_times(j);
                y = amplitude * sin(k*x) * cos(omega*t);
                plot(x, y, 'LineWidth', 2, 'Color', colors(j,:));
            end
            axis(standingWaveAxis);
            title('Standing Wave at Different Times');
            grid on;
            legend(arrayfun(@(t) sprintf('t = %.2f s', t), sample_times, 'UniformOutput', false));
            
            subplot(2,1,2);
            hold on;
            for j = 1:length(sample_times)
                t = sample_times(j);
                y = amplitude * sin(k*x - omega*t);
                plot(x, y, 'LineWidth', 2, 'Color', colors(j,:));
            end
            axis(travelingWaveAxis);
            title('Traveling Wave at Different Times');
            grid on;
            xlabel('Position (x)');
            
            result.title = 'Wave Propagation';
            result.description = sprintf('Standing and traveling waves with amplitude %.1f, wavelength %.1f, period %.1f s', amplitude, wavelength, period);
            
        case 'orbit'
            % Planetary orbit animation
            % Parameters for the orbit
            a = 1;  % Semi-major axis
            e = 0.5;  % Eccentricity
            
            % Set up the figure
            set(fig, 'Position', [100, 100, 800, 800]);
            
            % Compute the orbit
            theta = linspace(0, 2*pi, 1000);
            r = a * (1 - e^2) ./ (1 + e * cos(theta));
            x_orbit = r .* cos(theta);
            y_orbit = r .* sin(theta);
            
            % Define consistent axis limits
            orbitAxisLimits = [-a*(1+e)*1.2, a*(1+e)*1.2, -a*(1+e)*1.2, a*(1+e)*1.2];
            
            % Time settings (in terms of angle)
            theta_steps = linspace(0, 2*pi, num_frames);
            
            % Generate and save each frame
            for i = 1:num_frames
                clf;
                
                % Current angle
                current_theta = theta_steps(i);
                
                % Current position
                current_r = a * (1 - e^2) / (1 + e * cos(current_theta));
                current_x = current_r * cos(current_theta);
                current_y = current_r * sin(current_theta);
                
                % Plot the orbit and current position
                plot(x_orbit, y_orbit, 'b-', 'LineWidth', 1);
                hold on;
                
                % Plot the sun at the focus
                plot(0, 0, 'yo', 'MarkerSize', 20, 'MarkerFaceColor', 'y');
                
                % Plot the planet
                plot(current_x, current_y, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
                
                % Plot the trail
                if i > 1
                    % Previous positions
                    prev_thetas = theta_steps(1:i-1);
                    prev_r = a * (1 - e^2) ./ (1 + e * cos(prev_thetas));
                    prev_x = prev_r .* cos(prev_thetas);
                    prev_y = prev_r .* sin(prev_thetas);
                    
                    % Plot with decreasing opacity
                    for j = 1:length(prev_x)
                        % Opacity increases with recency - simulated by color intensity
                        alpha = j / length(prev_x);
                        % Use RGB without alpha channel
                        marker_color = [1, 1-alpha, 1-alpha]; % Red with varying intensity
                        plot(prev_x(j), prev_y(j), 'o', 'MarkerSize', 6, 'MarkerFaceColor', marker_color, 'MarkerEdgeColor', 'none');
                    end
                end
                
                % Configure the plot with consistent axis limits
                axis equal;
                axis(orbitAxisLimits);
                title(sprintf('Planetary Orbit (e = %.1f)', e));
                grid on;
                
                % Add annotations
                text(-a*(1+e)*1.1, -a*(1+e)*1.1, sprintf('Frame %d/%d', i, num_frames), 'FontSize', 10);
                
                % Save the frame
                frame_filename = fullfile(static_dir, sprintf('frame_%03d.png', i));
                frames{i} = frame_filename;
                print(fig, frame_filename, '-dpng', '-r100');
            end
            
            % Create a summary plot for the thumbnail
            clf;
            
            % Plot the complete orbit with planet positions
            plot(x_orbit, y_orbit, 'b-', 'LineWidth', 1.5);
            hold on;
            
            % Plot the sun
            plot(0, 0, 'yo', 'MarkerSize', 20, 'MarkerFaceColor', 'y');
            
            % Plot planets at equal time intervals
            sample_thetas = linspace(0, 2*pi, 8);
            for j = 1:length(sample_thetas)
                current_theta = sample_thetas(j);
                current_r = a * (1 - e^2) / (1 + e * cos(current_theta));
                current_x = current_r * cos(current_theta);
                current_y = current_r * sin(current_theta);
                
                % Plot with varying intensity instead of alpha
                intensity = 0.3 + 0.7 * j / length(sample_thetas);
                red_color = [1, 1-intensity, 1-intensity]; % From pink to red
                plot(current_x, current_y, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', red_color);
            end
            
            % Configure the plot with consistent axis limits
            axis equal;
            axis(orbitAxisLimits);
            title('Planetary Orbit Animation');
            grid on;
            
            result.title = 'Planetary Orbit';
            result.description = sprintf('Elliptical orbit with semi-major axis %.1f and eccentricity %.1f', a, e);
            
        case 'lissajous'
            % Lissajous curve animation
            t = linspace(0, 2*pi, 1000);
            a = 3;  % Frequency ratio (x-axis)
            b = 4;  % Frequency ratio (y-axis)
            
            % Phase varies with frame
            delta = linspace(0, pi, num_frames);
            
            % Create frames
            for i = 1:num_frames
                x = sin(a*t + delta(i));
                y = sin(b*t);
                
                % Plot
                clf;
                plot(x, y, 'g-', 'LineWidth', 2);
                axis([-1.2 1.2 -1.2 1.2]);
                grid on;
                axis equal;
                title(sprintf('Lissajous Curve (Phase = %.2f rad)', delta(i)));
                
                % Save frame
                frame_path = fullfile(static_dir, sprintf('frame_%03d.png', i));
                frames{i} = frame_path;
                saveas(gcf, frame_path);
            end
        case 'spiral'
            % Spiral formation animation
            t = linspace(0, 15, 1000);
            
            % Create frames
            for i = 1:num_frames
                % Calculate max time for this frame
                max_t = (i/num_frames) * 15;
                t_visible = t(t <= max_t);
                
                % Calculate spiral coordinates
                r = 0.1 * t_visible;
                x = r .* cos(t_visible);
                y = r .* sin(t_visible);
                
                % Plot
                clf;
                plot(x, y, 'm-', 'LineWidth', 2);
                axis([-1.2 1.2 -1.2 1.2]);
                grid on;
                axis equal;
                title(sprintf('Spiral Formation (t = %.2f)', max_t));
                
                % Save frame
                frame_path = fullfile(static_dir, sprintf('frame_%03d.png', i));
                frames{i} = frame_path;
                saveas(gcf, frame_path);
            end
        otherwise
            error('Unknown animation type. Try "pendulum", "wave", "orbit", "lissajous", or "spiral"');
    end
    
    % End of animation frame generation, debugging output
    fprintf('Animation completed, generated %d frames\n', length(frames));
    for i = 1:min(3, length(frames))
        fprintf('Frame %d: %s\n', i, frames{i});
    end
    
    % Save the summary plot as the thumbnail
    result.thumbnail = fullfile(static_dir, 'thumbnail.png');
    print(fig, result.thumbnail, '-dpng', '-r100');
    fprintf('Saved thumbnail: %s\n', result.thumbnail);
    
    % Create the result structure with URLs instead of file paths
    frame_urls = cell(1, num_frames);
    for i = 1:length(frames)
        % Convert the file path to a URL (/static/animation/frame_xxx.png)
        [~, name, ext] = fileparts(frames{i});
        frame_urls{i} = ['/static/animation/', name, ext];
    end
    
    result.frames = frame_urls;
    result.num_frames = num_frames;
    
    % Also convert thumbnail to URL
    [~, thumb_name, thumb_ext] = fileparts(result.thumbnail);
    result.thumbnail = ['/static/animation/', thumb_name, thumb_ext];
    
    % Add MATLAB signature
    axes('Position', [0.01, 0.01, 0.1, 0.05], 'Visible', 'off');
    text(0, 0, 'MATLAB', 'FontSize', 8, 'Color', [0.8, 0, 0], 'FontWeight', 'bold');
    
    % Thumbnail already saved and processed
    
    % Close the figure
    close(fig);
    
    % Final verification output
    fprintf('Animation result structure created with %d frames\n', length(result.frames));
end 