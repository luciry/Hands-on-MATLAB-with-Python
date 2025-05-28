import matlab.engine

# Start MATLAB engine
eng = matlab.engine.start_matlab()


eng.addpath(eng.genpath('C:\\Users\\lucac\\Documents\\GitHub\\Hands-on-MATLAB-with-Python\\Exercise'))


result = eng.simple_plot()

# Optionally, keep MATLAB open until the user closes the plot window
input("Press Enter to exit and close MATLAB...")

# Stop the MATLAB engine
eng.quit()
