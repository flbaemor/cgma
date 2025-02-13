const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/run-lexer', (req, res) => {
    const inputText = req.body.inputText;

    exec(`python cgmalexer.py "${inputText}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.json({ tokens: [], error: 'Error executing lexer.' });
        }

        try {
            const output = JSON.parse(stdout);
            res.json({ tokens: output.tokens, error: output.error || "" });
        } catch (parseError) {
            console.error('Parsing error:', parseError);
            res.json({ tokens: [], error: 'Invalid lexer output format.' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
