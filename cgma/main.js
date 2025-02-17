document.addEventListener('DOMContentLoaded', (event) => {
    const editor = document.getElementById('editor');
    const lineNumbers = document.getElementById('lineNumbers');

    // Function to update line numbers
    function updateLineNumbers() {
        const lines = editor.value.split('\n').length;
        lineNumbers.innerHTML = ''; // Clear existing line numbers
        for (let i = 1; i <= lines; i++) {
            lineNumbers.innerHTML += `<div>${i}</div>`;
        }
    }

    // Update line numbers on input
    editor.addEventListener('input', updateLineNumbers);

    // Synchronize scrolling of line numbers with textarea
    editor.addEventListener('scroll', () => {
        lineNumbers.scrollTop = editor.scrollTop;
    });

    // Initial update of line numbers
    updateLineNumbers();
});

async function runLexer() {
    const sourceCode = document.getElementById('editor').value;
    console.log("Running lexer with source code:", sourceCode);
    try {
        const response = await fetch('/api/lex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source_code: sourceCode })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Lexer response:", data);
        const tokensTableBody = document.getElementById('tokenBody');
        tokensTableBody.innerHTML = '';
        data.tokens.forEach(token => {
            const row = tokensTableBody.insertRow();
            const cellType = row.insertCell(0);
            const cellValue = row.insertCell(1);
            cellType.textContent = token.type;
            cellValue.textContent = token.value;
            cellValue.style.whiteSpace = 'pre'; // Ensure whitespace characters are displayed correctly
        });
        document.getElementById('error').textContent = data.errors.join('\n');
    } catch (error) {
        console.error("Error running lexer:", error);
    }
}

async function runParser() {
    const tokens = Array.from(document.getElementById('tokenBody').rows).map(row => ({
        type: row.cells[0].textContent,
        value: row.cells[1].textContent
    }));
    console.log("Running parser with tokens:", tokens);
    try {
        const response = await fetch('/api/parse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tokens: tokens })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Parser response:", data);
        document.getElementById('error').textContent = data.success ? 'Parsing successful!' : 'Parsing failed.';
    } catch (error) {
        console.error("Error running parser:", error);
    }
}

function runSemantic() {
    // Placeholder for semantic analysis functionality
    console.log("Semantic analysis not implemented yet.");
    document.getElementById('error').textContent = "Semantic analysis not implemented yet.";
}