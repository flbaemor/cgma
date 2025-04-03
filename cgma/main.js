document.addEventListener('DOMContentLoaded', async () => {
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.43.0/min/vs' } });

    require(['vs/editor/editor.main'], function () {

        monaco.languages.register({ id: "cgma" });

        monaco.languages.setMonarchTokensProvider("cgma", {
        tokenizer: {
            
            root: [
                [/\b(chungus|chudeluxe|forsen|forsencd|lwk|nocap|aura|sturdy)\b/, "type"],
                [/\b(hawk|tuah|lethimcook|jit|lil|plug)\b/, "control"],
                [/\b(yap|chat)\b/, "io"],
                [/\b(append|insert|remove|ts|taper)\b/, "function"],
                [/\b(continue|getout|back)\b/, "control1"],
                [/\b(npc|caseoh|fein)\b/, "keyword"],
                [/\b(true|false)\b/, "boolean"],
                [/\/\/.*/, "comment"],
                [/\/\*/, 'comment', '@comment'],
                [/\d+/, "number"],
                [/"[^"]*"/, "string"],
                [/'[^']*'/, "string"],
                [/[+\-*/<>!,&|]+/, "operator"],
                [/\b[a-zA-Z_]\w*(?=\()/, "functionIdentifier"],
                [/\b[a-zA-Z_]\w*\b/, "identifier"], // Identifiers
                [/[\{\}]/, "braces"],
                [/[\[\]]/, "bracket"],
                [/[\(\)]/, "parenthesis"],
            ],

            comment: [
            [/[^*]+/, 'comment'],
            [/\*\//, 'comment', '@pop'],
            [/\*/, 'comment'],
            ],
        },
    });

    monaco.languages.setLanguageConfiguration("cgma", {
        comments: {
            blockComment: ["/*", "*/"],
            lineComment: "//"          
        }
    });
    
        monaco.editor.defineTheme("myCustomTheme", {
        base: "vs-dark",
        inherit: true,
        rules: [
            { token: "keyword", foreground: "#B7B1F2"}, 
            { token: "type", foreground: "#75b4e0"},
            { token: "control", foreground: "#B7B1F2"},
            { token: "control1", foreground: "#ff79c6"},
            { token: "function", foreground: "#ff79c6"},
            { token: "io", foreground: "#8be9fd"},
            { token: "boolean", foreground: "#FFDCCC"},
            { token: "number", foreground: "#FFDCCC"},
            { token: "string", foreground: "#FFDCCC"},
            { token: "operator", foreground: "#FFFFFF"},
            { token: "identifier", foreground: "#FDB7EA", fontStyle: "bold"},
            { token: "functionIdentifier", foreground: "#ffb070", fontStyle: "bold"},
            { token: "braces", foreground: "#00ffe5", fontStyle: "bold"},
            { token: "bracket", foreground: "#47ff69"},
            { token: "parenthesis", foreground: "#47ff69"},
            { token: "comment", foreground: "#946893", fontStyle: "italic" },
        ],
            colors: {
                "editor.foreground": "#FFFFFF",
                "editor.background": "#4f134e",
                "editorCursor.foreground": "#FFFFFF",
                "editor.lineHighlightBackground": "#4a2949",
                "editorLineNumber.foreground": "#8e7b8b",
                "editorindentGuide.background": "#8e7b8b",
                "editorindentGuide.activebackground": "#946893",
                "scrollbarSlider.background": "#3c043c", 
                "scrollbarSlider.hoverBackground": "#5e045e", 
                "scrollbarSlider.activeBackground": "#90037b"
            }
        });

        window.editor = monaco.editor.create(document.getElementById('editor'), {
            value: `chungus skibidi(){\n\t//your code here\n\t\n\tback 0\n}`,
            language: 'cgma',
            theme: 'myCustomTheme',
            minimap: { enabled: false },
            overviewRulerLanes: 0,
            automaticLayout: true,
            newLineCharacter: "\n",
            suggest: {
                filterGraceful: false,
                showWords: false,
                enabled: false,
            },
            scrollbar: {
                vertical: "auto",
                horizontal: "auto",
                alwaysConsumeMouseWheel: false,
                verticalScrollbarSize: 10,
                horizontalScrollbarSize: 10,
            },

        });

        editor.onDidScrollChange(() => {
            document.getElementById('lineNumbers').scrollTop = editor.getScrollTop();
        });
    });
    document.querySelector('.run').addEventListener('click', runLexer);

});

document.querySelector(".widthResizer").addEventListener("mousedown", (e) => {
    e.preventDefault();
    document.addEventListener("mousemove", widthResize);
    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", widthResize);
    }, { once: true });
});

function widthResize(e) {
    let newWidth = e.clientX - document.querySelector(".textFieldCont").getBoundingClientRect().left;
    document.querySelector(".textFieldCont").style.width = `${newWidth}px`;
}

// Resizable Height
document.querySelector(".heightResizer").addEventListener("mousedown", (e) => {
    e.preventDefault();
    document.addEventListener("mousemove", heightResize);
    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", heightResize);
    }, { once: true });
});

function heightResize(e) {
    let newHeight = e.clientY - document.querySelector(".mainCont").getBoundingClientRect().top;
    document.querySelector(".mainCont").style.height = `${newHeight}px`;
}

async function runLexer() {
    const sourceCode = editor.getValue();
    console.log("Running lexer with source code:", sourceCode);
    
    try {
        const response = await fetch('/api/lex', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_code: sourceCode })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        console.log("Lexer response:", data);
        
        const tokensTableBody = document.getElementById('tokenBody');
        tokensTableBody.innerHTML = '';

        data.tokens.forEach(token => {
            const row = tokensTableBody.insertRow();
            row.insertCell(0).textContent = token.type.replace(/\n/g, "\\n");
            row.insertCell(1).textContent = token.value;
        });

        const errorBox = document.getElementById('errorText');
        errorBox.value = data.errors.length > 0 ? data.errors.join('\n') : 'Lexical analysis successful!';
    } catch (error) {
        console.error("Error running lexer:", error);
        document.getElementById('errorText').value = 'Error running lexical analysis.';
    }
}

async function runSyntax() {
    const sourceCode = editor.getValue();
    console.log("Running syntax with source code:", sourceCode);
    await runLexer();

    try {
        const response = await fetch('/api/parse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_code: sourceCode })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        console.log("Syntax response:", data);

        document.getElementById('errorText').value = data.success
            ? 'Syntax analysis successful!'
            : data.errors.join('\n');
    } catch (error) {
        console.error("Error running syntax:", error);
        document.getElementById('errorText').value = 'Error running syntax analysis.';
    }
}

async function runSemantic() {
    const errorBox = document.getElementById('errorText');
    errorBox.value = '';
    
    await runSyntax();
    if (errorBox.value !== 'Syntax analysis successful!') return;

    const sourceCode = editor.getValue();
    console.log("Running semantic analysis with source code:", sourceCode);
    
    try {
        const response = await fetch('/api/semantic', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_code: sourceCode })
        });

        if (!response.ok) throw new Error(`Semantic HTTP error! status: ${response.status}`);

        const data = await response.json();
        console.log("Semantic response:", data);

        errorBox.value = data.success ? 'Semantic analysis successful!' : data.errors.join('\n');
    } catch (error) {
        console.error("Error running semantic analysis:", error);
        errorBox.value = 'Error running semantic analysis.';
    }
}

function updateLineNumbers() {
    const lines = editor.getValue().split('\n').length;
    const lineNumbers = document.getElementById('lineNumbers');
    lineNumbers.innerHTML = '';

    for (let i = 1; i <= lines; i++) {
        lineNumbers.innerHTML += `<div>${i}</div>`;
    }
}
