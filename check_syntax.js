const fs = require('fs');

const html = fs.readFileSync('c:/Users/emroa/Downloads/SND/app/src/main/assets/index.html', 'utf8');

// Extract script content
const scriptMatch = html.match(/<script type="module">([\s\S]*?)<\/script>/);
if (!scriptMatch) {
    console.log('No script found');
    process.exit(1);
}

const jsCode = scriptMatch[1];
const lines = jsCode.split('\n');

console.log(`Total lines in script: ${lines.length}`);

// Try to find syntax errors by checking bracket/brace balance
let openBraces = 0;
let openBrackets = 0;
let openParens = 0;
let inString = false;
let inTemplate = false;
let stringChar = '';

for (let i = 0; i < Math.min(lines.length, 6220); i++) {
    const line = lines[i];
    
    // Check around line 6207
    if (i >= 6200 && i <= 6215) {
        console.log(`Line ${i}: ${line.substring(0, 100)}`);
    }
}
