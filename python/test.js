const spawn = require('child_process').spawn;

const sample = [4000, 10]
const pyProg = spawn('python', ['classifier.py', sample]);

pyProg.stdout.on('data', (data) => {
    console.log("GOT FROM PYTHON:", data.toString())
});

pyProg.stderr.on('data', (data) => {
    console.log("GOT FROM PYTHON ERR:", data.toString())
});