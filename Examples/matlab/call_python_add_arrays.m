% Example: Call a Python function from MATLAB
% Make sure Python is set up in MATLAB with pyenv

% Add two arrays using a Python function
a = [1, 2, 3];
b = [4, 5, 6];
pyResult = py.example_numpy.add_arrays(a, b);
matlabResult = double(pyResult);
disp('Sum from Python:');
disp(matlabResult);
