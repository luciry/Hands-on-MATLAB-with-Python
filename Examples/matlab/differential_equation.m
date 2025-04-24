function result = differential_equation(eq_type, t_max, num_points)
    % DIFFERENTIAL_EQUATION Solves and visualizes differential equations
    %   result = DIFFERENTIAL_EQUATION(eq_type, t_max, num_points)
    %
    %   Parameters:
    %     eq_type - Type of equation ('spring', 'pendulum', 'predator_prey', 'lorenz')
    %     t_max - Maximum simulation time
    %     num_points - Number of points to calculate
    
    % Set default parameters if not provided
    if nargin < 1, eq_type = 'spring'; end
    if ~ischar(eq_type), eq_type = 'spring'; end
    if nargin < 2, t_max = 10; end
    if nargin < 3, num_points = 100; end
    
    % Ensure we have minimum number of points
    num_points = max(num_points, 50);
    
    % Create time vector
    t = linspace(0, t_max, num_points);
    
    % Solve the selected differential equation
    figure('Visible', 'off');
    
    try
        switch lower(eq_type)
            case 'spring'
                % Spring-mass system: m*y'' + c*y' + k*y = 0
                % Parameters: mass m=1, damping c=0.5, spring constant k=4
                m = 1; c = 0.5; k = 4;
                
                % Solve spring-mass ODE manually without using ss
                % Convert to first-order system:
                % y1' = y2
                % y2' = -(k/m)*y1 - (c/m)*y2
                
                % Define ODE function
                spring_mass = @(t, y) [y(2); -(k/m)*y(1) - (c/m)*y(2)];
                
                % Solve with initial conditions y(0)=1, y'(0)=0
                options = odeset('RelTol', 1e-6, 'AbsTol', 1e-6);
                [~, y] = ode45(spring_mass, t, [1; 0], options);
                
                % Extract position and velocity
                position = y(:,1);
                velocity = y(:,2);
                
                % Plot solution
                subplot(2,1,1)
                plot(t, position, 'LineWidth', 2);
                title('Damped Spring-Mass System');
                xlabel('Time');
                ylabel('Position');
                grid on;
                
                subplot(2,1,2)
                plot(position, velocity, 'LineWidth', 2);
                title('Phase Portrait');
                xlabel('Position');
                ylabel('Velocity');
                grid on;
                
                result.equation = 'my" + cy'' + ky = 0';
                result.parameters = sprintf('m=%g, c=%g, k=%g', m, c, k);
                
            case 'pendulum'
                % Nonlinear pendulum: θ'' + (g/L)*sin(θ) = 0
                % Parameters: g=9.81, L=1
                g = 9.81; L = 1;
                
                % Define the ODE function
                pendulum = @(t, y) [y(2); -(g/L)*sin(y(1))];
                
                % Solve with more robust solver settings
                options = odeset('RelTol', 1e-6, 'AbsTol', 1e-6);
                
                % Solve for small angle (θ₀=0.1)
                [t_small, y_small] = ode45(pendulum, t, [0.1; 0], options);
                
                % Solve for large angle (θ₀=2)
                [t_large, y_large] = ode45(pendulum, t, [2; 0], options);
                
                % Plot solutions
                subplot(2,1,1)
                plot(t_small, y_small(:,1), 'b-', t_large, y_large(:,1), 'r-', 'LineWidth', 2);
                title('Pendulum Motion: Small vs Large Angle');
                xlabel('Time');
                ylabel('Angle (rad)');
                legend('Small Angle (θ₀=0.1)', 'Large Angle (θ₀=2)');
                grid on;
                
                subplot(2,1,2)
                plot(y_small(:,1), y_small(:,2), 'b-', y_large(:,1), y_large(:,2), 'r-', 'LineWidth', 2);
                title('Phase Portrait');
                xlabel('Angle (rad)');
                ylabel('Angular Velocity (rad/s)');
                legend('Small Angle (θ₀=0.1)', 'Large Angle (θ₀=2)');
                grid on;
                
                result.equation = 'θ" + (g/L)sin(θ) = 0';
                result.parameters = sprintf('g=%g, L=%g', g, L);
                
            case 'predator_prey'
                % Lotka-Volterra predator-prey model
                % dx/dt = αx - βxy
                % dy/dt = δxy - γy
                % where x = prey, y = predator
                
                % Parameters
                alpha = 1.1; beta = 0.4;
                delta = 0.1; gamma = 0.4;
                
                % Define the ODE function
                lotka_volterra = @(t, z) [alpha*z(1) - beta*z(1)*z(2); 
                                          delta*z(1)*z(2) - gamma*z(2)];
                
                % Initial conditions: 10 prey, 5 predators
                options = odeset('RelTol', 1e-6, 'AbsTol', 1e-6);
                [t_pp, z] = ode45(lotka_volterra, t, [10; 5], options);
                
                % Plot solutions
                subplot(2,1,1)
                plot(t_pp, z(:,1), 'g-', t_pp, z(:,2), 'r-', 'LineWidth', 2);
                title('Predator-Prey Dynamics');
                xlabel('Time');
                ylabel('Population');
                legend('Prey', 'Predator');
                grid on;
                
                subplot(2,1,2)
                plot(z(:,1), z(:,2), 'LineWidth', 2);
                title('Phase Portrait: Predator vs Prey');
                xlabel('Prey Population');
                ylabel('Predator Population');
                grid on;
                
                result.equations = 'dx/dt = αx - βxy, dy/dt = δxy - γy';
                result.parameters = sprintf('α=%g, β=%g, δ=%g, γ=%g', alpha, beta, delta, gamma);
                
            case 'lorenz'
                % Lorenz system:
                % dx/dt = σ(y - x)
                % dy/dt = x(ρ - z) - y
                % dz/dt = xy - βz
                
                % Parameters (classic values for chaos)
                sigma = 10; rho = 28; beta = 8/3;
                
                % Define the ODE function
                lorenz = @(t, xyz) [sigma*(xyz(2) - xyz(1)); 
                                   xyz(1)*(rho - xyz(3)) - xyz(2); 
                                   xyz(1)*xyz(2) - beta*xyz(3)];
                
                % Initial condition with more robust solver settings
                options = odeset('RelTol', 1e-6, 'AbsTol', 1e-6);
                [t_lorenz, xyz] = ode45(lorenz, t, [1; 1; 1], options);
                
                % 3D plot of the Lorenz attractor
                plot3(xyz(:,1), xyz(:,2), xyz(:,3), 'LineWidth', 1.5);
                title('Lorenz Attractor');
                xlabel('x'); ylabel('y'); zlabel('z');
                grid on;
                view(-110, 30);  % Set view angle
                
                result.equations = 'dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz';
                result.parameters = sprintf('σ=%g, ρ=%g, β=%g', sigma, rho, beta);
                
            otherwise
                % Default to spring-mass if unknown
                warning('Unknown equation type "%s". Using spring-mass system instead.', eq_type);
                
                % Simple spring-mass system without Control System Toolbox
                m = 1; c = 0.5; k = 4;
                spring_mass = @(t, y) [y(2); -(k/m)*y(1) - (c/m)*y(2)];
                
                % Solve with initial conditions y(0)=1, y'(0)=0
                options = odeset('RelTol', 1e-6, 'AbsTol', 1e-6);
                [~, y] = ode45(spring_mass, t, [1; 0], options);
                
                % Extract position and velocity
                position = y(:,1);
                velocity = y(:,2);
                
                % Plot solution
                subplot(2,1,1)
                plot(t, position, 'LineWidth', 2);
                title('Damped Spring-Mass System');
                xlabel('Time');
                ylabel('Position');
                grid on;
                
                subplot(2,1,2)
                plot(position, velocity, 'LineWidth', 2);
                title('Phase Portrait');
                xlabel('Position');
                ylabel('Velocity');
                grid on;
                
                result.equation = 'my" + cy'' + ky = 0';
                result.parameters = sprintf('m=%g, c=%g, k=%g', m, c, k);
        end
    catch ME
        % Handle errors gracefully by using a proper warning format 
        if ~isempty(ME.identifier)
            warning(ME.identifier, 'Error: %s', ME.message);
        else
            warning('MATLAB:DiffEq:SolverError', 'Error: %s', ME.message);
        end
        
        % Create a simple placeholder plot
        subplot(2,1,1)
        x = linspace(0, 2*pi, 100);
        y = sin(x) .* exp(-x/5);
        plot(x, y, 'LineWidth', 2);
        title(sprintf('Simple Oscillation (fallback for %s)', eq_type));
        xlabel('Time');
        ylabel('Amplitude');
        grid on;
        
        subplot(2,1,2)
        text(0.5, 0.5, sprintf('Could not solve "%s" equation:\n%s', eq_type, ME.message), ...
            'HorizontalAlignment', 'center', 'FontSize', 12);
        axis off;
        
        result.equation = 'Error solving differential equation';
        result.parameters = ME.message;
    end
    
    % Add MATLAB signature
    axes('Position', [0.01, 0.01, 0.1, 0.05], 'Visible', 'off');
    text(0, 0, 'MATLAB', 'FontSize', 8, 'Color', [0.8, 0, 0], 'FontWeight', 'bold');
end 