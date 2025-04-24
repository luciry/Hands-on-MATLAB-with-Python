function result = matrix_operation(operation, size, seed)
    % MATRIX_OPERATION Performs various matrix operations with visualization
    %   result = MATRIX_OPERATION(operation, size, seed)
    %   
    %   Parameters:
    %     operation - Type of operation ('eigenvalues', 'svd', or 'matrix')
    %     size - Size of the random matrix (NxN)
    %     seed - Random seed for reproducibility
    
    % Set default parameters if not provided
    if nargin < 1, operation = 'eigenvalues'; end
    if ~ischar(operation), operation = 'eigenvalues'; end
    if nargin < 2, size = 3; end
    if nargin < 3, seed = 42; end
    
    % Set random seed for reproducibility
    rng(seed);
    
    % Generate random matrix
    A = rand(size, size);
    
    % Create figure (invisible for web app)
    figure('Visible', 'off');
    
    % Perform the requested operation
    switch lower(operation)
        case 'eigenvalues'
            % Calculate eigenvalues
            e = eig(A);
            
            % Plot eigenvalues in complex plane
            scatter(real(e), imag(e), 100, 'filled');
            grid on;
            title(sprintf('Eigenvalues of %dx%d Random Matrix', size, size));
            xlabel('Real Part');
            ylabel('Imaginary Part');
            
            % Add origin lines
            hold on;
            plot([-1, 1], [0, 0], 'k-', 'LineWidth', 0.5);
            plot([0, 0], [-1, 1], 'k-', 'LineWidth', 0.5);
            hold off;
            
            % Set axis equal and adjust limits
            axis equal;
            xlim([-1, 1]);
            ylim([-1, 1]);
            
            % Return eigenvalues in result
            result.eigenvalues = e;
            
        case 'svd'
            % Perform Singular Value Decomposition
            [~, S, ~] = svd(A);
            s = diag(S);
            
            % Plot singular values
            stem(1:length(s), s, 'filled', 'LineWidth', 2);
            grid on;
            title(sprintf('Singular Values of %dx%d Random Matrix', size, size));
            xlabel('Index');
            ylabel('Singular Value');
            
            % Return singular values in result
            result.singular_values = s;
            
        otherwise % Default: just show the matrix
            % Display the matrix as an image
            imagesc(A);
            colormap('jet');
            colorbar;
            title(sprintf('%dx%d Random Matrix', size, size));
            axis equal;
            axis tight;
            
            % Return the matrix in result
            result.matrix = A;
    end
    
    % Add MATLAB watermark (to show it's from MATLAB)
    axes('Position', [0.01, 0.01, 0.1, 0.05], 'Visible', 'off');
    text(0, 0, 'Made with MATLAB', 'FontSize', 8, 'Color', [0.8, 0, 0]);
end 