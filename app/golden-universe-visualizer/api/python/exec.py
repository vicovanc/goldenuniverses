"""
Vercel Serverless Python Execution Function
This function runs Python code in Vercel's Python runtime
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import io
import traceback
import time
from contextlib import redirect_stdout, redirect_stderr
import numpy as np
import scipy
from mpmath import mp

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests for Python code execution"""
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            code = data.get('code', '')

            if not code:
                self.send_error_response(400, 'No code provided')
                return

            # Execute the Python code
            result = self.execute_python_code(code)

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                'success': result['success'],
                'data': {
                    'output': result['output'],
                    'error': result.get('error'),
                    'exitCode': 0 if result['success'] else 1,
                    'executionTime': result['executionTime']
                }
            }

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_error_response(500, str(e))

    def execute_python_code(self, code):
        """Execute Python code and capture output"""
        start_time = time.time()
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

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

    def send_error_response(self, status_code, message):
        """Send an error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = {
            'success': False,
            'error': message
        }

        self.wfile.write(json.dumps(response).encode())