import tkinter as tk
from tkinter import ttk
import cgmalexer  # Importing your lexer module

def process_input():
    """
    Process the input text using cgmalexer and update the output and error sections.
    """
    input_text = input_textbox.get("1.0", tk.END).strip()  # Get input from the text box
    tokens, error = cgmalexer.run('<file>', input_text)

    # Display tokens produced before the error
    token_output_textbox.config(state=tk.NORMAL)
    token_output_textbox.delete("1.0", tk.END)
    
    # Format and display the tokens produced
    if tokens:  # If there are tokens, display them
        token_output_textbox.insert(tk.END, "\n".join(map(str, tokens)))
    else:  # If no valid tokens
        token_output_textbox.insert(tk.END, "\n".join(map(str, tokens)))
        
    token_output_textbox.config(state=tk.DISABLED)

    # Display the error if present
    error_output_textbox.config(state=tk.NORMAL)
    error_output_textbox.delete("1.0", tk.END)
    if error:  # Show error details
        error_output_textbox.insert(tk.END, error.as_string())
    else:
        error_output_textbox.insert(tk.END, "No errors found.")
    error_output_textbox.config(state=tk.DISABLED)

# GUI Application
root = tk.Tk()
root.title("CGMA Lexer Program")
root.geometry("800x600")
root.resizable(False, False)

# Configure grid
root.grid_rowconfigure(0, weight=6)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=7)

# Input Section
input_frame = ttk.LabelFrame(root, text="Program Input")
input_frame.grid(row=0, column=0, rowspan=2, padx=1, pady=1, sticky="nsew")

input_textbox = tk.Text(input_frame, wrap=tk.WORD)
input_textbox.pack(fill="both", expand=True, padx=1, pady=1)

# Token Output Section
token_output_frame = ttk.LabelFrame(root, text="Token Output")
token_output_frame.grid(row=0, column=1, padx=1, pady=1, sticky="nsew")

token_output_textbox = tk.Text(token_output_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#e8f5e9")
token_output_textbox.pack(fill="both", expand=True, padx=1, pady=1)

# Process Button
process_button = ttk.Button(root, text="TOKENIZE", command=process_input)
process_button.grid(row=1, column=1, pady=1)

# Error Output Section
error_output_frame = ttk.LabelFrame(root, text="Error Handling")
error_output_frame.grid(row=2, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")

error_output_textbox = tk.Text(error_output_frame, wrap=tk.WORD, height=10, state=tk.DISABLED, bg="#ffebee")
error_output_textbox.pack(fill="both", expand=True, padx=1, pady=1)

# Run the application
root.mainloop()