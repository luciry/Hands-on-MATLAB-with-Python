from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
import time
import json
import tempfile
from io import BytesIO
import matlab.engine
import shutil
from PIL import Image

# Add path to find MATLAB example code
examples_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Examples')
matlab_examples_dir = os.path.join(examples_dir, 'matlab')
python_examples_dir = os.path.join(examples_dir, 'python')
sys.path.append(python_examples_dir)

# Add the webapp directory to the path if matlab_bridge import fails
try:
    from webapp.matlab_bridge import call_matlab_function, get_matlab_source
except ImportError:
    # Try relative import 
    try:
        from .matlab_bridge import call_matlab_function, get_matlab_source, get_matlab_engine
    except ImportError:
        # Last resort: direct import with path modification
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        from matlab_bridge import call_matlab_function, get_matlab_source, get_matlab_engine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbolic')
def symbolic_page():
    return render_template('symbolic.html')

@app.route('/source_code/<function_name>')
def source_code(function_name):
    """Get the source code of a MATLAB function"""
    code = get_matlab_source(function_name)
    if code:
        return jsonify({
            'status': 'success',
            'source_code': code,
            'function_name': function_name
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Source code for {function_name} not found'
        })

# Here we can find POST requests to MATLAB functions
# They work like this:
# 1. We get the function name and parameters from the request
# 2. We call the function through our bridge
# 3. We return the result

@app.route('/simple_plot', methods=['POST'])
def simple_plot():
    try:
        # Get parameters from the request
        data = request.json
        x_min = data.get('x_min', -10)
        x_max = data.get('x_max', 10)
        num_points = data.get('num_points', 100)
        
        # Generate a simple plot using matplotlib
        x = np.linspace(x_min, x_max, num_points)
        y = np.sin(x)
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(x, y)
        plt.title('Simple Sine Wave')
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.grid(True)
        
        # Convert plot to base64 string for embedding in HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return jsonify({
            'status': 'success',
            'plot': plot_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/advanced_plot', methods=['POST'])
def advanced_plot():
    try:
        # Get parameters from the request
        data = request.json
        
        # Call the Python implementation in matlab_bridge.py
        result = call_matlab_function('advanced_plot', data)
        
        # Return the result
        return jsonify({
            'status': 'success',
            'plot': result.get('plot'),
            'source_code': result.get('source_code')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/differential_equation', methods=['POST'])
def differential_equation():
    try:
        # Get parameters from the request
        data = request.json
        
        # Call the function through our bridge
        result = call_matlab_function('differential_equation', data)
        
        # Return the result
        return jsonify({
            'status': 'success',
            'plot': result.get('plot'),
            'source_code': result.get('source_code'),
            'equation': result.get('equation'),
            'equations': result.get('equations'),
            'parameters': result.get('parameters')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/image_processing', methods=['POST'])
def image_processing():
    try:
        # Get parameters from the request
        data = request.json
        
        # Call the function through our bridge
        result = call_matlab_function('image_processing', data)
        
        # Return the result
        return jsonify({
            'status': 'success',
            'plot': result.get('plot'),
            'source_code': result.get('source_code'),
            'operation': result.get('operation'),
            'methods': result.get('methods')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })



@app.route('/source_code/<function_name>')
def get_source_code(function_name):
    """Retrieve the source code for a specific MATLAB function"""
    try:
        # Sanitize function name (basic security measure)
        safe_chars = set('abcdefghijklmnopqrstuvwxyz_')
        if not all(c in safe_chars for c in function_name.lower()):
            return jsonify({
                'status': 'error',
                'message': 'Invalid function name'
            }), 400
        
        # Get source code
        source_code = get_matlab_source(function_name)
        
        if source_code is not None:
            return jsonify({
                'status': 'success',
                'source_code': source_code
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Source code for {function_name} not found'
            }), 404
    except Exception as e:
        print(f"Error in source_code endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/matrix_operation', methods=['POST'])
def matrix_operation():
    try:
        # Get parameters from the request
        data = request.json
        
        # Call the function through our bridge
        result = call_matlab_function('matrix_operation', data)
        
        # Return the result
        return jsonify({
            'status': 'success',
            'plot': result.get('plot'),
            'source_code': result.get('source_code'),
            'operation_info': {
                'title': result.get('operation_title', data.get('operation_type', 'Matrix Operation')),
                'details': result.get('operation_details', '')
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })



@app.route('/api/image_processing', methods=['GET'])
def api_image_processing():
    try:
        # Get parameters from the request
        noise_level = request.args.get('noise_level', 0.2)
        operation = request.args.get('operation', 'edge')
        
        # Call the MATLAB function through our bridge
        result = call_matlab_function('image_processing', 
                                    {'operation': operation, 'noise_level': float(noise_level)})
        
        # Return a properly structured response for the frontend
        if 'plot' in result:
            return jsonify({
                'noisy_image': result['plot'],  # Use the same image for now
                'filtered_image': result['plot'],
                'operation': result.get('operation', 'Image Processing'),
                'methods': result.get('methods', '')
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'No image data received'
            })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/differential_equation', methods=['GET'])
def api_differential_equation():
    try:
        # Get parameters from the request
        eq_type = request.args.get('eq_type', 'spring')
        t_max = request.args.get('t_max', 10)
        num_points = request.args.get('num_points', 100)
        
        # Call the MATLAB function through our bridge
        result = call_matlab_function('differential_equation', 
                                    {'eq_type': eq_type, 
                                     't_max': float(t_max), 
                                     'num_points': int(num_points)})
        
        # Return a properly structured response
        if 'plot' in result:
            return jsonify({
                'plot': result['plot'],
                'equation': result.get('equation', result.get('equations', '')),
                'parameters': result.get('parameters', '')
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'No plot data received'
            })
    except Exception as e:
        import traceback
        print(f"Animation error: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/animation', methods=['GET'])
def api_animation():
    try:
        animation_type = request.args.get('animation_type', 'pendulum')
        num_frames = request.args.get('num_frames', 20)
        result = call_matlab_function('animation', {'animation_type': animation_type, 'num_frames': int(num_frames)})
        
        # Debug what we got back from MATLAB
        print(f"Raw result type: {type(result)}")
        if isinstance(result, dict):
            print(f"Result keys: {list(result.keys())}")
            if 'data' in result:
                print(f"Result contains 'data' key, type: {type(result['data'])}")
                if isinstance(result['data'], dict) and 'frames' in result['data']:
                    print(f"result['data']['frames'] type: {type(result['data']['frames'])}, length: {len(result['data']['frames']) if hasattr(result['data']['frames'], '__len__') else 'no length'}")
            if 'frames' in result:
                print(f"Direct 'frames' key exists, type: {type(result['frames'])}, length: {len(result['frames']) if hasattr(result['frames'], '__len__') else 'no length'}")
                if len(result['frames']) > 0:
                    print(f"First frame: {result['frames'][0]}")
        
        frames = []
        if isinstance(result, dict):
            if 'frames' in result and isinstance(result['frames'], (list, tuple)):
                frames = [str(f) for f in result['frames']]
            elif 'data' in result and isinstance(result['data'], dict) and 'frames' in result['data']:
                frames = [str(f) for f in result['data']['frames']]


        response_data = {
            'frames': frames,
            'thumbnail': result.get('thumbnail', ''),
            'description': result.get('description', ''),
            'num_frames': len(frames),
            'title': result.get('title', 'Animation') if isinstance(result, dict) else ''
        }
        print(f"Returning animation response: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/symbolic', methods=['POST'])
def symbolic_operation():
    try:
        # Get parameters from the request
        data = request.get_json()
        expression = data.get('expression')
        operation = data.get('operation')

        # Create parameters for symbolic operations - need to use positional arguments instead of keyword arguments for MATLAB
        # The call_matlab_function handles conversion between Python objects and MATLAB objects
        # For our symbolic_math function, we have these parameters: (expression, operation, plot_path)
        
        # Prepare plot path for plot operation
        plot_path = None
        if operation == 'plot':
            plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'plots')
            os.makedirs(plots_dir, exist_ok=True)
            plot_filename = f'symbolic_plot_{int(time.time())}.png'
            plot_path = os.path.join(plots_dir, plot_filename).replace('\\', '/')

        # Use the existing call_matlab_function mechanism that's already imported and working
        # Call with positional arguments instead of a dictionary for MATLAB compatibility
        print("Calling MATLAB function: symbolic_math with params: {params}")
        print("Expression: ", expression)
        print("Operation: ", operation)
        print("Plot path: ", plot_path)
        result = call_matlab_function('symbolic_math', {
            'arg1': expression,  # First positional arg: expression
            'arg2': operation,   # Second positional arg: operation
            'arg3': plot_path    # Third positional arg: plot_path (None for non-plot operations)
        })

        if result and 'status' in result and result['status'] == 'success':
            return jsonify({
                'status': 'success',
                'result': result.get('result', ''),
                'latex': result.get('latex', ''),
                'plot': result.get('plot', None)
            })
        else:
            # Handle error from MATLAB function
            return jsonify({
                'status': 'error',
                'message': result.get('message', 'Error processing symbolic math operation')
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })
@app.route('/matlab_plot', methods=['POST'])
def matlab_plot():
    try:
        # Get parameters from the request
        data = request.json
        function_name = data.get('function', 'simple_plot')
        params = data.get('params', {})
        
        # Call the MATLAB function through our bridge
        result = call_matlab_function(function_name, params)
        
        # Flatten the result structure for the frontend
        response = {'status': 'success'}
        if isinstance(result, dict):
            for key, value in result.items():
                response[key] = value
        
        return jsonify(response)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 