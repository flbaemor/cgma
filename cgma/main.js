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
            event.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
    
            this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 1;
        } else if (event.key === 'Enter') {
            event.preventDefault();
            const start = this.selectionStart;
            const textBeforeCursor = this.value.substring(0, start);
            const textAfterCursor = this.value.substring(start);
            
            // Get the previous line's indentation
            const previousLine = textBeforeCursor.split('\n').pop();
            const indentation = previousLine.match(/^\s*/)[0];
    
            // Insert newline with the same indentation
            this.value = textBeforeCursor + '\n' + indentation + textAfterCursor;
            this.selectionStart = this.selectionEnd = start + indentation.length + 1;
    
            // **Trigger line number update**
            updateLineNumbers();
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


const widthResizer = document.querySelector(".widthResizer");
const textFieldCont = document.querySelector(".textFieldCont");
const heightResizer = document.querySelector(".heightResizer");
const mainCont = document.querySelector(".mainCont");

widthResizer.addEventListener("mousedown", (e) => {
    e.preventDefault();
    document.addEventListener("mousemove", widthResize);
    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", widthResize);
    }, { once: true });
});

function widthResize(e) {
    let newWidth = e.clientX - textFieldCont.getBoundingClientRect().left;
    textFieldCont.style.width = `${newWidth}px`;
};

heightResizer.addEventListener("mousedown", (e) => {
    e.preventDefault();
    document.addEventListener("mousemove", heightResize);
    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", heightResize);
    }, { once: true });
});

function heightResize(e) {
    let newHeight = e.clientY - mainCont.getBoundingClientRect().top;
    mainCont.style.height = `${newHeight}px`;
};

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
            cellValue.style.whiteSpace = 'pre';
        });
        
        const errorBox = document.getElementById('errorText');
        if (data.errors.length > 0) {
            errorBox.value = data.errors.join('\n');
            //errorBox.style.color = 'red';
        } else {
            errorBox.value = 'Lexical analysis successful!';
            //errorBox.style.color = 'green';
        }
    } catch (error) {
        console.error("Error running lexer:", error);
        document.getElementById('errorText').value = 'Error running lexical analysis.';
    }
}

async function runSyntax() {
    const sourceCode = document.getElementById('editor').value;
    console.log("Running syntax with source code:", sourceCode);
    runLexer();
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
        
        const errorBox = document.getElementById('errorText');
        
        if (data.success) {
            errorBox.value = 'Syntax analysis successful!';
            //errorBox.style.color = 'green';
        } else {
            errorBox.value = data.errors.join('\n');
            //errorBox.style.color = 'red';
        }
    } catch (error) {
        console.error("Error running syntax:", error);
        document.getElementById('errorText').value = 'Error running syntax analysis.';
    }
}

async function runSemantic() {
    const errorBox = document.getElementById('errorText');
    await runSyntax();
    if (errorBox.value != 'Syntax analysis successful!') {
        return; // Stop execution if syntax errors exist
    }

    const sourceCode = document.getElementById('editor').value;
    console.log("Running semantic analysis with source code:", sourceCode);
    try {
        const response = await fetch('/api/semantic', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_code: sourceCode })
        });

        if (!response.ok) {
            throw new Error(`Semantic HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Semantic response:", data);

        if (!data.success) {
            errorBox.value = data.errors.join('\n');
        } else {
            errorBox.value = 'Semantic analysis successful!';
        }
    } catch (error) {
        console.error("Error running semantic analysis:", error);
        errorBox.value = 'Error running semantic analysis.';
    }
}