// Test script to verify Python execution API
const fetch = require('node-fetch');

async function testPythonExecution() {
  const apiUrl = 'http://localhost:3001/api/python/exec';

  const testCode = `
import json
import sys

# Test calculation
result = {
    "test": "success",
    "value": 42 * 3.14159,
    "python_version": sys.version.split()[0]
}

print(json.dumps(result, indent=2))
`;

  try {
    console.log('Testing Python execution API...');

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code: testCode,
        filename: 'test.py'
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    console.log('\nResponse:', JSON.stringify(data, null, 2));

    if (data.success && data.data && data.data.output) {
      console.log('\n✅ Python execution API is working!');
      console.log('Output from Python:', data.data.output);
    } else {
      console.log('\n❌ Python execution returned but with issues');
    }
  } catch (error) {
    console.error('\n❌ Error testing Python API:', error.message);
    console.error('Make sure the backend server is running on port 3001');
  }
}

testPythonExecution();