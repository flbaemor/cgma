document.querySelector('.run').addEventListener('click', () => {
    const inputText = document.getElementById('editor').value;

    fetch('/run-lexer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputText: inputText }),
    })
    .then(response => response.json())
    .then(data => {
        updateTokenTable(data.tokens);
        document.getElementById('error').value = data.errors.length > 0 ? data.errors.join("\n") : "";
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error').value = "Failed to process input.";
    });
});

function updateTokenTable(tokens) {
    const tokenBody = document.getElementById('tokenBody');
    tokenBody.innerHTML = ""; // Clear previous tokens

    if (tokens.length === 0) {
        tokenBody.innerHTML = "<tr><td colspan='2'>No tokens found</td></tr>";
        return;
    }

    tokens.forEach(token => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${token.type}</td><td>${token.value}</td>`;
        tokenBody.appendChild(row);
    });
}
const editor = document.getElementById("editor");
const lineNumbers = document.getElementById("lineNumbers");

// Function to update line numbers
function updateLineNumbers() {
    const lines = editor.value.split("\n").length; // Count lines in editor
    let numbersHTML = "";

    for (let i = 1; i <= lines; i++) {
        numbersHTML += `<div>${i}</div>`; // Add line number
    }

    lineNumbers.innerHTML = numbersHTML;
}

// Event listener to update line numbers while typing
editor.addEventListener("input", updateLineNumbers);
editor.addEventListener("scroll", () => {
    lineNumbers.scrollTop = editor.scrollTop; // Sync scroll
});

// Initialize line numbers on page load
updateLineNumbers();