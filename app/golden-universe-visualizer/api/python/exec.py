"""
Vercel Serverless Python Execution Function
This function runs Python code in Vercel's Python runtime
"""

import json
import sys
import io
import traceback
import time
from contextlib import redirect_stdout, redirect_stderr

def handler(request):
    """
    Vercel serverless function handler for Python code execution
    """
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    # Handle preflight request
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    # Only handle POST requests
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': 'Method not allowed'
            })
        }

    try:
        # Parse request body
        body = json.loads(request.body) if request.body else {}
        code = body.get('code', '')

        if not code:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'No code provided'
                })
            }

        # Execute the Python code
        result = execute_python_code(code)

        # Return success response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': result['success'],
                'data': {
                    'output': result['output'],
                    'error': result.get('error'),
                    'exitCode': 0 if result['success'] else 1,
                    'executionTime': result['executionTime']
                }
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }


def execute_python_code(code):
    """Execute Python code and capture output"""
    start_time = time.time()
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()

    # Import dependencies here to ensure they're available
    import numpy as np
    from mpmath import mp, mpf

    # Set up Golden Universe constants and functions
    setup_code = """
import numpy as np
from mpmath import mp, mpf
import json

# Set precision
mp.dps = 50

# Golden Universe Constants
PHI = mp.phi  # Golden ratio
PI = mp.pi
E = mp.e
PHI_SQ = PHI ** 2

# Physical constants
M_P_MeV = mpf('938.272088')  # Proton mass in MeV
M_E_MeV = mpf('0.51099895')  # Electron mass in MeV
ALPHA = mpf('0.0072973525693')  # Fine structure constant

# Winding numbers
N_E = 137  # Electron winding number
DELTA_E = mpf('0.036')  # Electron correction
NU_E = N_E + DELTA_E  # Effective electron winding

# Helper functions
def calculate_electron_mass(nu):
    '''Calculate electron mass using Golden Universe formula'''
    l_omega = 2 * mp.sqrt((nu / PHI_SQ) + (PHI_SQ / (4 * nu)))
    m_electron = M_P_MeV / (l_omega ** 11)
    return float(m_electron)

def calculate_newtons_g():
    '''Calculate Newton's gravitational constant'''
    g_value = 1 / (PHI ** 34)
    return float(g_value)

def calculate_fine_structure():
    '''Calculate fine structure constant'''
    alpha = 1 / 137.036
    return alpha

def calculate_resonance(N, phi_sq):
    '''Calculate resonance for given N'''
    k_res = N * phi_sq
    delta = k_res - round(k_res)
    return k_res, delta

def calculate_winding_length(p, q):
    '''Calculate winding length for given p,q'''
    return 2 * mp.sqrt((abs(p) / PHI_SQ) + (PHI_SQ * abs(q) / 4))

def to_json(obj):
    '''Convert object to JSON-serializable format'''
    if isinstance(obj, (mp.mpf, mp.mpc)):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: to_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_json(item) for item in obj]
    else:
        return obj
"""

    try:
        # Create a combined code block
        full_code = setup_code + "\n\n# User code:\n" + code

        # Create a local namespace for execution
        namespace = {}

        # Redirect stdout and stderr
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            exec(full_code, namespace)

        # Get the output
        output = output_buffer.getvalue()

        # If there's a result variable in namespace, add it to output
        if 'result' in namespace:
            if output:
                output += "\n"
            result_json = json.dumps(namespace['result'], default=str)
            output += result_json

        execution_time = int((time.time() - start_time) * 1000)

        return {
            'success': True,
            'output': output.strip(),
            'executionTime': execution_time
        }

    except Exception as e:
        error_output = error_buffer.getvalue()
        if not error_output:
            error_output = traceback.format_exc()

        execution_time = int((time.time() - start_time) * 1000)

        return {
            'success': False,
            'output': output_buffer.getvalue().strip(),
            'error': error_output,
            'executionTime': execution_time
        }