from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import json
import tempfile
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
        from .matlab_bridge import call_matlab_function, get_matlab_source
    except ImportError:
        # Last resort: direct import with path modification
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        from matlab_bridge import call_matlab_function, get_matlab_source

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/animation', methods=['POST'])
def animation_endpoint():
    try:
        # Get parameters from the request
        data = request.json
        
        # Call the function through our bridge
        result = call_matlab_function('animation', data)
        
        # Return the result
        return jsonify({
            'status': 'success',
            'frames': result.get('frames'),
            'thumbnail': result.get('thumbnail'),
            'title': result.get('title'),
            'description': result.get('description'),
            'num_frames': result.get('num_frames'),
            'source_code': result.get('source_code')
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
        
        # Important fix: Flatten the result structure for the frontend
        response = {'status': 'success'}
        # Add all keys from result to the response
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
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/animation', methods=['GET'])
def api_animation():
    try:
        # Get parameters from the request
        animation_type = request.args.get('animation_type', 'pendulum')
        num_frames = request.args.get('num_frames', 20)
        speed = request.args.get('speed', 1)
        
        print(f"Animation request: type={animation_type}, frames={num_frames}, speed={speed}")
        
        # Call the MATLAB function through our bridge
        result = call_matlab_function('animation', 
                                    {'animation_type': animation_type, 
                                     'num_frames': int(num_frames)})
        
        print(f"Raw animation result keys: {result.keys()}")
        
        # Check all possible data formats from the MATLAB function
        frames = None
        
        # Format 1: Direct 'frames' key (ideal case)
        if 'frames' in result and result['frames']:
            frames = result['frames']
            print(f"Found {len(frames)} frames in 'frames' key")
            
        # Format 2: Nested inside 'data' key (actual case based on logs)
        elif 'data' in result:
            data_obj = result['data']
            print(f"Found 'data' key, type: {type(data_obj)}")
            
            # Examine data object attributes
            if hasattr(data_obj, 'frames'):
                print(f"data.frames exists, type: {type(data_obj.frames)}")
                # Check if it's a cell array or list
                try:
                    if hasattr(data_obj.frames, '_data'):  # MATLAB cell array
                        frames = [frame for frame in data_obj.frames]
                    else:  # Regular list or array
                        frames = list(data_obj.frames)
                    print(f"Extracted {len(frames)} frames from data.frames")
                except Exception as e:
                    print(f"Error extracting frames: {e}")
            
            # Just in case, print all available attributes
            print("All attributes of data object:")
            for attr in dir(data_obj):
                if not attr.startswith('_'):
                    print(f"  {attr}: {type(getattr(data_obj, attr))}")
        
        # Return animation data with detailed logging
        if frames and len(frames) > 0:
            print(f"Animation generated successfully: {len(frames)} frames")
            # For debugging, print the first frame path
            if len(frames) > 0:
                print(f"First frame: {frames[0][:100]}...")
                
            response_data = {
                'frames': frames,
                'thumbnail': result.get('thumbnail', frames[0] if frames else None),
                'title': getattr(result.get('data', {}), 'title', 'Animation') if 'data' in result else result.get('title', 'Animation'),
                'description': getattr(result.get('data', {}), 'description', '') if 'data' in result else result.get('description', '')
            }
            return jsonify(response_data)
        else:
            # Check if there's any fallback animation data
            print(f"No frames found in result: {result.keys()}")
            return jsonify({
                'status': 'error',
                'message': 'No animation frames received'
            })
    except Exception as e:
        import traceback
        print(f"Animation error: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 