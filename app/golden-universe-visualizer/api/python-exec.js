// Vercel Serverless Function for Python Execution
// This function executes Python code in Vercel's serverless environment

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed'
    });
  }

  const { code, filename = 'script.py' } = req.body;

  if (!code) {
    return res.status(400).json({
      success: false,
      error: 'No code provided'
    });
  }

  try {
    // In Vercel, we can't spawn processes directly
    // We need to use a different approach

    // Option 1: Use Pyodide via edge function (client-side)
    // This is handled by the fallback in the frontend

    // Option 2: Use a Python runtime API or external service
    // For now, we'll return a message indicating to use the Pyodide fallback

    return res.status(200).json({
      success: false,
      error: 'Python execution not available in serverless. Please use client-side Pyodide.',
      fallback: 'pyodide'
    });

  } catch (error) {
    console.error('Serverless Python execution error:', error);
    return res.status(500).json({
      success: false,
      error: error.message || 'Failed to execute Python code'
    });
  }
}