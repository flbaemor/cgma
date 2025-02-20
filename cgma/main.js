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

    document.getElementById('editor').addEventListener('keydown', function(event) {
        if (event.key === 'Tab') {
            event.preventDefault(); // Prevent moving to the next element
            const start = this.selectionStart;
            const end = this.selectionEnd;
    
            // Insert tab character at cursor position
            this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
    
            // Move cursor position after inserted tab
            this.selectionStart = this.selectionEnd = start + 1;
        }
    });

    // Add event listeners for navigation links
    document.getElementById('lexerLink').addEventListener('click', (e) => {
        e.preventDefault();
        runLexer();
    });

    document.getElementById('syntaxLink').addEventListener('click', (e) => {
        e.preventDefault();
        runSyntax();
    });

    document.getElementById('semanticLink').addEventListener('click', (e) => {
        e.preventDefault();
        runSemantic();
    });

    document.querySelector('.run').addEventListener('click', runLexer);
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

async function runSyntax() {
    const sourceCode = document.getElementById('editor').value;
    console.log("Running syntax with source code:", sourceCode);
    
    try {
        const response = await fetch('/api/parse', {
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
        console.log("Syntax response:", data);
        
        const errorBox = document.getElementById('error');
        errorBox.value = data.success ? 'Parsing successful!' : 'Parsing failed.'; // Use `.value` for textarea
        errorBox.style.color = data.success ? 'green' : 'red'; // Color feedback for success/failure
    } catch (error) {
        console.error("Error running syntax:", error);
        document.getElementById('error').value = 'Error running syntax analysis.';
    }
}


async function runSemantic() {
    const sourceCode = document.getElementById('editor').value;
    console.log("Running semantic analysis with source code:", sourceCode);
    // Placeholder for semantic analysis logic
    document.getElementById('error').textContent = 'Semantic analysis not implemented yet.';
}