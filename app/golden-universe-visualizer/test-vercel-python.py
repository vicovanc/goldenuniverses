#!/usr/bin/env python3
"""
Test script for Vercel Python serverless function
Tests the actual Golden Universe calculations
"""

import requests
import json

def test_python_execution(api_url):
    """Test the Python execution API with Golden Universe calculations"""

    test_cases = [
        {
            "name": "Simple calculation",
            "code": "print(42 * 3.14159)"
        },
        {
            "name": "Electron mass calculation",
            "code": """
result = calculate_electron_mass(NU_E)
print(f"Electron mass: {result} MeV")
"""
        },
        {
            "name": "Newton's G calculation",
            "code": """
result = calculate_newtons_g()
print(f"Newton's G: {result}")
"""
        },
        {
            "name": "Fine structure calculation",
            "code": """
result = calculate_fine_structure()
print(f"Fine structure constant: {result}")
print(f"Inverse: {1/result}")
"""
        },
        {
            "name": "Winding number calculation",
            "code": """
# Calculate for electron
p, q = -41, 70
l_omega = calculate_winding_length(p, q)
print(f"Winding length for p={p}, q={q}: {l_omega}")

# Calculate mass
m_electron = float(M_P_MeV / (l_omega ** 11))
print(f"Calculated electron mass: {m_electron} MeV")
print(f"Experimental: {M_E_MeV} MeV")
"""
        }
    ]

    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print(f"{'='*60}")

        try:
            response = requests.post(
                api_url,
                headers={'Content-Type': 'application/json'},
                json={'code': test['code']},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    output = data.get('data', {}).get('output', '')
                    print(f"✅ Success!")
                    print(f"Output:\n{output}")
                    if data.get('data', {}).get('executionTime'):
                        print(f"Execution time: {data['data']['executionTime']}ms")
                else:
                    print(f"❌ Failed!")
                    print(f"Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                print(response.text)

        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    import sys

    # Default to local development server
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        # Test local development by default
        api_url = "http://localhost:3001/api/python/exec"
        print(f"Testing local API: {api_url}")
        print("To test Vercel, run: python test-vercel-python.py https://your-app.vercel.app/api/python/exec")

    test_python_execution(api_url)