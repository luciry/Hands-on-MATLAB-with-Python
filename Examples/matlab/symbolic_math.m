function result = symbolic_math(params)
% SYMBOLIC_MATH Perform symbolic math operations
%   This function handles various symbolic math operations including:
%   - simplify
%   - differentiate
%   - integrate
%   - solve
%   - plot
%
%   Input: params struct with fields:
%     - expression: The mathematical expression to process as a string
%     - operation: One of 'simplify', 'differentiate', 'integrate', 'solve', 'plot'
%     - plot_path (optional): Path to save the plot image (for 'plot' operation)
%
%   Output: result struct with fields:
%     - status: 'success' or 'error'
%     - result: Result of the operation as a string
%     - latex: LaTeX representation of the result
%     - plot: Base64 encoded plot image (for 'plot' operation)
%     - message: Error message (if status is 'error')

    % Initialize result struct
    result = struct('status', 'error', 'message', '', 'result', '', 'latex', '', 'plot', '');
    
    try
        % Get parameters
        if ~isfield(params, 'expression') || ~isfield(params, 'operation')
            result.message = 'Missing required parameters: expression or operation';
            return;
        end
        
        expression = params.expression;
        operation = params.operation;
        
        % Create symbolic variable and parse expression
        syms x;
        try
            expr = eval(['symengine, ''', expression, ''';']);
        catch
            try
                % Fallback if the first approach doesn't work
                evalc(['expr = ', expression, ';']);
            catch err
                result.message = ['Error parsing expression: ', err.message];
                return;
            end
        end
        
        % Perform the requested operation
        switch operation
            case 'simplify'
                res = simplify(expr);
                result.result = char(res);
                result.latex = latex(res);
                
            case 'differentiate'
                res = diff(expr, x);
                result.result = char(res);
                result.latex = latex(res);
                
            case 'integrate'
                res = int(expr, x);
                result.result = char(res);
                result.latex = latex(res);
                
            case 'solve'
                res = solve(expr == 0, x);
                if numel(res) > 1
                    % Convert array to string
                    result.result = '[';
                    for i = 1:numel(res)
                        if i > 1
                            result.result = [result.result, ', '];
                        end
                        result.result = [result.result, char(res(i))];
                    end
                    result.result = [result.result, ']'];
                    result.latex = latex(res);
                else
                    result.result = char(res);
                    result.latex = latex(res);
                end
                
            case 'plot'
                % Check if plot_path is provided
                if ~isfield(params, 'plot_path')
                    result.message = 'Missing required parameter: plot_path';
                    return;
                end
                
                % Create plot
                figure('Visible', 'off');
                fplot(expr, [-10, 10], 'LineWidth', 2);
                title(expression, 'Interpreter', 'none');
                xlabel('x');
                ylabel('y');
                grid on;
                
                % Save plot to file
                saveas(gcf, params.plot_path);
                
                % Read back the file and encode as base64
                fid = fopen(params.plot_path, 'rb');
                if fid == -1
                    result.message = 'Error reading plot file';
                    return;
                end
                
                bytes = fread(fid, inf, 'uint8');
                fclose(fid);
                
                % Convert to base64 string
                encoded = base64encode(bytes);
                result.plot = encoded;
                result.result = ['Plot created for ', expression];
                result.latex = result.result;
                
            otherwise
                result.message = ['Unknown operation: ', operation];
                return;
        end
        
        % Operation completed successfully
        result.status = 'success';
        
    catch err
        result.message = ['MATLAB error: ', err.message];
    end
end

function encoded = base64encode(data)
    % Encode binary data as base64 string
    % Implementation varies based on MATLAB version
    
    try
        % Try using built-in base64 functions (newer MATLAB versions)
        encoded = matlab.net.base64encode(data);
    catch
        try
            % Alternative approach for older MATLAB versions
            encoded = base64encode_fallback(data);
        catch
            % Last resort - return error placeholder
            encoded = 'Error: Unable to encode image';
        end
    end
end

function encoded = base64encode_fallback(data)
    % Fallback base64 encoding for older MATLAB versions
    % Define base64 encoding table
    chars = ['A':'Z', 'a':'z', '0':'9', '+', '/'];
    
    % Pad data to multiple of 3
    padding = mod(3 - mod(length(data), 3), 3);
    data = [data; zeros(padding, 1)];
    
    % Convert every 3 bytes into 4 base64 characters
    encoded = '';
    for i = 1:3:length(data)
        chunk = data(i:i+2);
        n = bitor(bitshift(chunk(1), 16), bitor(bitshift(chunk(2), 8), chunk(3)));
        
        % Extract 6-bit chunks and convert to base64 characters
        idx1 = bitshift(n, -18) + 1;
        idx2 = bitand(bitshift(n, -12), 63) + 1;
        idx3 = bitand(bitshift(n, -6), 63) + 1;
        idx4 = bitand(n, 63) + 1;
        
        encoded = [encoded, chars(idx1), chars(idx2), chars(idx3), chars(idx4)];
    end
    
    % Add padding characters
    if padding > 0
        encoded(end-padding+1:end) = repmat('=', 1, padding);
    end
end
