import matlab.engine
eng = matlab.engine.start_matlab()
if eng.exist(function_name, nargout=1) >= 2:  # 2 means it's a file
    print(f"Calling MATLAB function: {function_name} with params: {params}")
    # Convert the params to MATLAB format and call the function
    if function_name == "simple_plot":
        x_min = params.get('x_min', -10)
        x_max = params.get('x_max', 10)
        num_points = params.get('num_points', 100)
        result = eng.simple_plot(float(x_min), float(x_max), float(num_points))
tf = eng.isprime(37)
print(tf)