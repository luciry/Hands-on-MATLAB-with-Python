function result = image_processing(operation, noise_level)
    % IMAGE_PROCESSING Demonstrates MATLAB's image processing capabilities
    %   result = IMAGE_PROCESSING(operation, noise_level)
    %
    %   Parameters:
    %     operation - Type of operation ('edge', 'filter', 'segment', 'transform')
    %     noise_level - Level of noise to add (0-1)
    
    % Set default parameters if not provided
    if nargin < 1, operation = 'edge'; end
    if ~ischar(operation), operation = 'edge'; end
    if nargin < 2, noise_level = 0.2; end
    
    % Create a test image without using Image Processing Toolbox functions
    [x, y] = meshgrid(linspace(-3, 3, 256), linspace(-3, 3, 256));
    r = sqrt(x.^2 + y.^2);
    I = (1 + sin(r))/2;
    
    % Scale to 0-1 range manually (replacing mat2gray)
    I_min = min(I(:));
    I_max = max(I(:));
    I = (I - I_min) / (I_max - I_min);
    
    % Ensure noise level is in valid range
    noise_level = max(0, min(noise_level, 1));
    
    % Add noise to the image - simplified without using imnoise
    J = I + noise_level * randn(size(I));
    J = min(max(J, 0), 1);  % Clip to [0,1] range
    
    % Process image based on selected operation
    figure('Visible', 'off');
    
    switch lower(operation)
        case 'edge'
            % Simple edge detection without using edge()
            % Use gradient approximation
            [Gx, Gy] = gradient(J);
            edges_manual = sqrt(Gx.^2 + Gy.^2);
            edges_threshold = edges_manual > 0.2;
            
            % Display results
            subplot(2,2,1)
            imshow(I)
            title('Original Image')
            
            subplot(2,2,2)
            imshow(J)
            title(sprintf('Noisy Image (σ = %.1f)', noise_level))
            
            subplot(2,2,3)
            imshow(edges_manual)
            title('Gradient Magnitude')
            
            subplot(2,2,4)
            imshow(edges_threshold)
            title('Thresholded Edges')
            
            result.operation = 'Edge detection';
            result.methods = 'Gradient-based edge detection';
            
        case 'filter'
            % Simple filtering without using specialized functions
            
            % Mean filter (basic implementation)
            kernel_size = 5;
            K_mean = J;
            for i = kernel_size:size(J,1)-kernel_size
                for j = kernel_size:size(J,2)-kernel_size
                    neighborhood = J(i-2:i+2, j-2:j+2);
                    K_mean(i,j) = mean(neighborhood(:));
                end
            end
            
            % Display results
            subplot(2,2,1)
            imshow(I)
            title('Original Image')
            
            subplot(2,2,2)
            imshow(J)
            title(sprintf('Noisy Image (σ = %.1f)', noise_level))
            
            subplot(2,2,3)
            imshow(K_mean)
            title('Mean Filter (Basic)')
            
            subplot(2,2,4)
            % Create another visualization
            [Gx, Gy] = gradient(K_mean);
            G_mag = sqrt(Gx.^2 + Gy.^2);
            imshow(G_mag)
            title('Gradient of Filtered Image')
            
            result.operation = 'Filtering';
            result.methods = 'Basic mean filtering';
            
        case 'segment'
            % Simple segmentation without specialized functions
            
            % Simple thresholding
            level = 0.5;  % Fixed threshold
            bw = J > level;
            
            % Simple region visualization
            labels = zeros(size(J));
            [labels, num_regions] = bwlabel_simple(bw);
            
            % Display results
            subplot(2,2,1)
            imshow(I)
            title('Original Image')
            
            subplot(2,2,2)
            imshow(J)
            title('Preprocessed Image')
            
            subplot(2,2,3)
            imshow(bw)
            title(sprintf('Thresholding (level = %.2f)', level))
            
            subplot(2,2,4)
            imshow(labels/max(labels(:)))
            title(sprintf('Region Labeling (%d regions)', num_regions))
            
            result.operation = 'Segmentation';
            result.methods = 'Thresholding, Connected Components';
            
        case 'transform'
            % Simple frequency domain visualization without specialized functions
            
            % Basic Fourier transform
            F = fft2(J);
            F_shifted = fftshift(F); % Center the transform
            magnitude = log(1 + abs(F_shifted));
            magnitude_scaled = magnitude / max(magnitude(:));
            
            % Display results
            subplot(2,2,1)
            imshow(I)
            title('Original Image')
            
            subplot(2,2,2)
            imshow(J)
            title(sprintf('Noisy Image (σ = %.1f)', noise_level))
            
            subplot(2,2,3)
            imshow(magnitude_scaled, [])
            title('FFT Magnitude (log scale)')
            
            subplot(2,2,4)
            % Show inverse FFT
            J_restored = real(ifft2(F));
            imshow(J_restored)
            title('Inverse FFT')
            
            result.operation = 'Transforms';
            result.methods = 'Fourier Transform';
            
        otherwise
            % Default to edge detection
            warning('Unknown operation "%s". Using edge detection.', operation);
            
            [Gx, Gy] = gradient(J);
            edges_manual = sqrt(Gx.^2 + Gy.^2);
            edges_threshold = edges_manual > 0.2;
            
            subplot(2,2,1)
            imshow(I)
            title('Original Image')
            
            subplot(2,2,2)
            imshow(J)
            title(sprintf('Noisy Image (σ = %.1f)', noise_level))
            
            subplot(2,2,3)
            imshow(edges_manual)
            title('Gradient Magnitude')
            
            subplot(2,2,4)
            imshow(edges_threshold)
            title('Thresholded Edges')
            
            result.operation = 'Edge detection';
            result.methods = 'Gradient-based edge detection';
    end
    
    % Add MATLAB signature
    axes('Position', [0.01, 0.01, 0.1, 0.05], 'Visible', 'off');
    text(0, 0, 'MATLAB', 'FontSize', 8, 'Color', [0.8, 0, 0], 'FontWeight', 'bold');
end

% Simple connected components labeling
function [labels, num_regions] = bwlabel_simple(bw)
    labels = zeros(size(bw));
    current_label = 0;
    
    for i = 1:size(bw, 1)
        for j = 1:size(bw, 2)
            if bw(i,j) == 1 && labels(i,j) == 0
                current_label = current_label + 1;
                % Use flood fill to label connected region
                labels = flood_fill(bw, labels, i, j, current_label);
            end
        end
    end
    
    num_regions = current_label;
end

% Simple flood fill algorithm
function labels = flood_fill(bw, labels, i, j, label_value)
    % Check bounds
    if i < 1 || i > size(bw, 1) || j < 1 || j > size(bw, 2)
        return;
    end
    
    % Check if pixel should be filled
    if bw(i,j) == 0 || labels(i,j) ~= 0
        return;
    end
    
    % Fill pixel
    labels(i,j) = label_value;
    
    % Recursive fill for 4-connected neighbors
    % This is very inefficient but simple for demonstration
    if i > 10 && j > 10 && i < size(bw,1)-10 && j < size(bw,2)-10
        % Limited depth for safety
        labels = flood_fill(bw, labels, i+1, j, label_value);
        labels = flood_fill(bw, labels, i-1, j, label_value);
        labels = flood_fill(bw, labels, i, j+1, label_value);
        labels = flood_fill(bw, labels, i, j-1, label_value);
    end
end 