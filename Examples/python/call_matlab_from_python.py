# Example: Call MATLAB from Python using MATLAB Engine API
# Requires MATLAB and the MATLAB Engine for Python installed
import matlab.engine

eng = matlab.engine.start_matlab()
result = eng.sqrt(16.0)
print('Square root of 16 from MATLAB:', result)
eng.quit()
