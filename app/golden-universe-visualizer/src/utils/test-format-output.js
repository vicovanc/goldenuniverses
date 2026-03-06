// Test script for formatOutput function
// This tests the formatting of derivation output

// The formatOutput function from PythonExecutor
const formatOutput = (text) => {
  // First, add line breaks before capital letters that come after numbers/scientific notation
  // This handles cases like "3.5710002800e+03Coupling:" -> "3.5710002800e+03\nCoupling:"
  let formatted = text.replace(/([0-9]|[0-9]e[+-][0-9]+)([A-Z])/g, '$1\n$2');

  // Also add line breaks before common term patterns
  // Handle patterns like "term: value" when they're concatenated
  formatted = formatted.replace(/([\d.e+-]+)([A-Z][a-z]+\s*term:)/g, '$1\n$2');

  // Handle "Total" or "Final" patterns that might be concatenated
  formatted = formatted.replace(/([\d.e+-]+)(Total|Final)/g, '$1\n$2');

  // Clean up any double line breaks that might have been introduced
  formatted = formatted.replace(/\n\n+/g, '\n');

  return formatted;
};

// Test with your example
const testInput = "Geometric term: 3.5710002800e+03Coupling: 5.7368237744e-03Kinetic term: 7.5962104833e+03Interaction: 5.5469479626e-01Total Lagrangian: 2.7128050578e+07Final Lagrangian density: 2.712805057839857e+07";

console.log("Original output:");
console.log(testInput);
console.log("\n" + "=".repeat(50) + "\n");

const formattedOutput = formatOutput(testInput);
console.log("Formatted output:");
console.log(formattedOutput);
console.log("\n" + "=".repeat(50) + "\n");

// Show each line separately
console.log("Lines in formatted output:");
formattedOutput.split('\n').forEach((line, index) => {
  console.log(`Line ${index + 1}: ${line}`);
});

// Test with more edge cases
console.log("\n" + "=".repeat(50) + "\n");
console.log("Testing edge cases:");

const testCases = [
  "Value: 1.5e+03Alpha: 0.00729Beta: 2.3e-05",
  "Result1: 123.456Result2: 789.012Final: 999.999",
  "Constant: 2.998e+08Mass: 9.109e-31Charge: 1.602e-19",
];

testCases.forEach((test, index) => {
  console.log(`\nTest ${index + 1}:`);
  console.log("Input:  " + test);
  console.log("Output:\n" + formatOutput(test));
});