function result = advanced_plot(function_type, amplitude, frequency, phase, x_min, x_max, num_points)
    % ADVANCED_PLOT Creates various waveform plots with adjustable parameters
    %   result = ADVANCED_PLOT(function_type, amplitude, frequency, phase, x_min, x_max, num_points)
    %   
    %   Parameters:
    %     function_type - Type of function to plot ('sin', 'cos', 'tan', 'square')
    %     amplitude - Amplitude of the wave
    %     frequency - Frequency of the wave
    %     phase - Phase shift of the wave
    %     x_min, x_max - Range of x-axis
    %     num_points - Number of points to plot
    
    % Set default parameters if not provided
    if nargin < 1, function_type = 'sin'; end
    if ~ischar(function_type), function_type = 'sin'; end
    if nargin < 2, amplitude = 1; end
    if nargin < 3, frequency = 1; end
    if nargin < 4, phase = 0; end
    if nargin < 5, x_min = -10; end
    if nargin < 6, x_max = 10; end
    if nargin < 7, num_points = 100; end
    
    % Generate x values
    x = linspace(x_min, x_max, num_points);
    
    % Generate y values based on function type
    switch lower(function_type)
        case 'sin'
            y = amplitude * sin(frequency * x + phase);
            title_text = sprintf('Sine Wave: %g·sin(%gx + %g)', amplitude, frequency, phase);
        case 'cos'
            y = amplitude * cos(frequency * x + phase);
            title_text = sprintf('Cosine Wave: %g·cos(%gx + %g)', amplitude, frequency, phase);
        case 'tan'
            y = amplitude * tan(frequency * x + phase);
            % Clip extreme values for better visualization
            y = min(max(y, -10), 10);
            title_text = sprintf('Tangent Wave: %g·tan(%gx + %g)', amplitude, frequency, phase);
        case 'square'
            y = amplitude * sign(sin(frequency * x + phase));
            title_text = sprintf('Square Wave: amplitude=%g, freq=%g, phase=%g', amplitude, frequency, phase);
        otherwise
            y = zeros(size(x));
            title_text = 'Unknown function type';
    end
    
    % Create plot with MATLAB's enhanced visualization
    figure('Visible', 'off');  % Create invisible figure (for web app)
    plot(x, y, 'LineWidth', 2);
    title(title_text, 'Interpreter', 'tex');
    xlabel('X axis');
    ylabel('Y axis');
    grid on;
    
    % Add MATLAB-specific enhancements
    ax = gca;
    ax.XAxisLocation = 'origin';
    ax.YAxisLocation = 'origin';
    ax.Box = 'off';
    
    % Return result (not used in this case as plot is returned via Python bridge)
    result = struct('status', 'success');
end 