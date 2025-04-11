document.addEventListener('DOMContentLoaded', async () => {

    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.43.0/min/vs',
        'xterm': 'https://cdn.jsdelivr.net/npm/xterm/lib',
        'xterm-addon-fit': 'https://cdn.jsdelivr.net/npm/xterm-addon-fit/lib/xterm-addon-fit',
     } });

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
            value: `skibidi{\n\t//your code here\n\t\n}`,
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
    });

    require(['vs/editor/editor.main', 'xterm/xterm', 'xterm-addon-fit'], function (_, Xterm, FitAddon) {

        const term = new Xterm.Terminal({
          cursorBlink: true,
          cursorStyle: 'bar',
          scrollback: 1000,
          theme: {
            background: '#3c043c',
            foreground: '#FFFFFF',
            cursor: '#FFFFFF',
            FontFace: 'monospace',
            fontStyle: 'bold',
          },
        });
        
    
        term.open(document.getElementById('terminal'));
        const fitAddon = new FitAddon.FitAddon(); // ✅ Create the fit addon
        term.loadAddon(fitAddon);                 // ✅ Load it into the terminal
        fitAddon.fit(); 
        setTimeout(() => term.focus(), 100);
        term.write('Terminal Ready\r\n');
      
        let userInput = '';
        let waitingForInput = false;
        let inputCallback = null;
      
        term.onData(e => {
          if (!waitingForInput) return;
      
          if (e === '\r') {
            term.write('\r\n');
            waitingForInput = false;
            if (inputCallback) inputCallback(userInput);
            userInput = '';
          } else if (e === '\u007f') {
            if (userInput.length > 0) {
              userInput = userInput.slice(0, -1);
              term.write('\b \b');
            }
          } else {
            userInput += e;
            term.write(e);
          }
        });
      
        function waitForInput(promptText = '') {
          return new Promise(resolve => {
            term.write(promptText);
            term.focus();
            waitingForInput = true;
            userInput = '';
            inputCallback = resolve;
          });
        }

        window.runLexer = async function () {
            const sourceCode = editor.getValue();
            console.log("Running lexer with source code:", sourceCode);
        
            term.clear();
            term.write('Running lexer...\r\n');
        
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
                    row.insertCell(0).textContent = token.type.replace(/\n/g, "\\n").replace("neg", "- (negative)");
                    row.insertCell(1).textContent = token.value;
                });
        
                if (data.errors.length > 0) {
                    term.write('Lexical Errors:\r\n');
                    data.errors.forEach(err => {
                        term.write(`[Error] ${err}\r\n`);
                    });
                } else {
                    term.write('Lexical analysis successful!\r\n');
                    return true;
                }
        
            } catch (error) {
                console.error("Error running lexer:", error);
                term.write('Error running lexical analysis.\r\n');
                return false;
            }
        };

        window.runSyntax = async function () {
            const sourceCode = editor.getValue();
            console.log("Running syntax with source code:", sourceCode);
          
            const lexerSuccess = await runLexer();
            if (!lexerSuccess) {
                return;
            }
            
            await new Promise(resolve => setTimeout(resolve, 10));
            term.clear();
            term.write('\rRunning syntax analysis...\r\n');
          
            try {
              const response = await fetch('/api/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source_code: sourceCode })
              });
          
              if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          
              const data = await response.json();
              console.log("Syntax response:", data);
          
              if (data.success) {
                term.write('Syntax analysis successful!\r\n');
                return true;
              } else {
                term.write('Syntax Errors:\r\n');
                data.errors.forEach(err => {
                term.write(`[Error] ${err}\r\n`);
                });
              }
          
            } catch (error) {
              console.error("Error running syntax:", error);
              term.write('Error running syntax analysis.\r\n');
              return false;
            }
        };

        window.runSemantic = async function () {
            const sourceCode = editor.getValue();
            console.log("Running semantic analysis with source code:", sourceCode);
          
            const syntaxSuccess = await runSyntax();
            
            if (!syntaxSuccess) {
                return;
            }

            await new Promise(resolve => setTimeout(resolve, 10));
            term.clear();
            term.write('\rRunning semantic analysis...\r\n');
          
            try {
              const response = await fetch('/api/semantic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source_code: sourceCode })
              });
          
              if (!response.ok) throw new Error(`Semantic HTTP error! status: ${response.status}`);
          
              const data = await response.json();
              console.log("Semantic response:", data);
          
              if (data.success) {
                term.write('Semantic analysis successful!\r\n');
                return true;
              } else {
                term.write('Semantic Errors:\r\n');
                data.errors.forEach(err => {
                  term.write(`[Error] ${err}\r\n`);
                });
              }
          
            } catch (error) {
              console.error("Error running semantic analysis:", error);
              term.write('Error running semantic analysis.\r\n');
              return false;
            }
        };
          
        runCode = async function () {
            term.clear(); // ✅ Start with a clean terminal
            term.write('Running program...\r\n');
          
            const semanticSuccess = await runSemantic(); // Run semantic analysis first
            
            if (!semanticSuccess) {
                return;
            }

            await new Promise(resolve => setTimeout(resolve, 10));
            term.clear();

            const sourceCode = editor.getValue();
          
            try {
              const response = await fetch('/api/output', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source_code: sourceCode })
              });
          
              const data = await response.json();
          
              if (!data.success) {
                term.write('Runtime Error:\r\n');
                if (data.errors) {
                  data.errors.forEach(err => {
                    term.write(`${err}\r\n`);
                  });
                }
                return;
              }
          
              if (data.input_required) {
                const input = await waitForInput(data.prompt);
                userInputs[data.prompt.trim()] = input;
                return;
              }
          
              if (data.output) {
                const outputLines = data.output.split('\n');
                outputLines.forEach(line => {
                  term.write(line + '\r\n');
                });
              }
          
            } catch (error) {
              console.error("Error running source code:", error);
              term.write('Error running source code.\r\n');
            }
        };
      });
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

function toggleDropdown() {
    const menu = document.getElementById("dropdown-menu");
    menu.classList.toggle("hidden");
  }
  
  // Hide dropdown if clicked outside
  document.addEventListener("click", function (e) {
    const dropdown = document.querySelector(".dropdown");
    const menu = document.getElementById("dropdown-menu");
  
    if (!dropdown.contains(e.target)) {
      menu.classList.add("hidden");
    }
  });


