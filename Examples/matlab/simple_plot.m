function result = simple_plot(x_min, x_max, num_points)
    % SIMPLE_PLOT Creates a simple sine wave plot
    %   result = SIMPLE_PLOT(x_min, x_max, num_points) creates a plot of sin(x)
    %   with x ranging from x_min to x_max with num_points points
    
    % Set default parameters if not provided
    if nargin < 1, x_min = -10; end
    if nargin < 2, x_max = 10; end
    if nargin < 3, num_points = 100; end
    
    % Generate data
    x = linspace(x_min, x_max, num_points);
    y = sin(x);
    
    % Create plot
    figure('Visible', 'off');  % Create invisible figure (for web app)
    plot(x, y, 'LineWidth', 2);
    title('Sine Wave (MATLAB Implementation)');
    xlabel('X axis');
    ylabel('Y axis');
    grid on;
    
    % Return result (not used in this case as plot is returned via Python bridge)
    result = struct('status', 'success');
end 