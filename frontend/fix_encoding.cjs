const fs = require('fs');
let text = fs.readFileSync('src/App.tsx', 'utf8');

// The text was read as windows-1252 (or latin1) and saved as utf8.
// This means a character like 'ó' (U+00F3, UTF-8 C3 B3) was read as two characters:
// \xC3 (Ã) and \xB3 (³). Then it was saved as UTF-8 string "Ã³".
// To fix, we can encode the string back to latin1 bytes, then decode as utf8!

let fixed;
try {
  const buffer = Buffer.from(text, 'latin1');
  fixed = buffer.toString('utf8');
  
  // Verify it worked: does it contain 'Bóng đá'?
  if (fixed.includes('Bóng đá')) {
     fs.writeFileSync('src/App.tsx', fixed, 'utf8');
     console.log('Fixed double encoding!');
  } else {
     console.log('Did not find expected characters after fix.');
  }
} catch (e) {
  console.log('Error:', e);
}
