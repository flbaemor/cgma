import tkinter as tk
from tkinter import ttk
import cgmalexer  # Importing your lexer module

def process_input():
    """
    Process the input text using cgmalexer and update the output and error sections.
    """
    input_text = input_textbox.get("1.0", tk.END).strip()  # Get input from the text box
    tokens, errors = cgmalexer.run('<file>', input_text)

    # Clear the previous tokens
    for item in token_output_tree.get_children():
        token_output_tree.delete(item)
    
    # Insert new tokens into the treeview
    if tokens:  # If there are tokens, display them
        for token in tokens:
            token_output_tree.insert("", "end", values=(token.type, token.value), tags=('bg',))
    else:  # If no valid tokens
        token_output_tree.insert("", "end", values=("", ""), tags=('bg',))

    # Display the errors if present
    error_output_textbox.config(state=tk.NORMAL)
    error_output_textbox.delete("1.0", tk.END)
    if errors:  # Show error details
        for error in errors:
            error_output_textbox.insert(tk.END, error.as_string() + "\n")
    else:
        error_output_textbox.insert(tk.END, "No errors found.")
    error_output_textbox.config(state=tk.DISABLED)

# GUI Application
root = tk.Tk()
root.title("CGMA Lexer Program")
root.geometry("1100x600")
root.resizable(True, True)
root.configure(bg="#292929")

# Configure grid
root.grid_rowconfigure(0, weight=6)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=7)

# Create a style for the LabelFrame
style = ttk.Style()
style.configure("Custom.TLabelframe", background="#292929")
style.configure("Custom.TLabelframe.Label", background="#292929", foreground="#ffffff", font=('Courier', 15, 'bold'))  # Set text color to white

# Input Section
input_frame = ttk.LabelFrame(root, text="PROGRAM INPUT", style="Custom.TLabelframe")
input_frame.grid(row=0, column=0, rowspan=2, padx=3, pady=3, sticky="nsew")

input_textbox = tk.Text(input_frame, wrap=tk.WORD, bg="#534857", fg="#ffffff", insertbackground="#ffffff", font=('Consolas', 11,))
input_textbox.pack(fill="both", expand=True, padx=3, pady=3)

# Token Output Section
token_output_frame = ttk.LabelFrame(root, text="TOKEN OUTPUT", style="Custom.TLabelframe")
token_output_frame.grid(row=0, column=1, padx=1, pady=1, sticky="nsew")

# Create a style for the Treeview
style.configure("Custom.Treeview", background="#534857", foreground="#ffffff", fieldbackground="#534857", font=('Consolas', 11))
style.configure("Custom.Treeview.Heading", background="#000000", foreground="#000000", font=('Courier', 12, 'bold'))


# Create a Treeview widget for displaying tokens in a table format
token_output_tree = ttk.Treeview(token_output_frame, columns=("Type", "Token"), show="headings", style="Custom.Treeview")
token_output_tree.heading("Type", text="Type", anchor="center")
token_output_tree.heading("Token", text="Token", anchor="center")
token_output_tree.column("Type", anchor="center")
token_output_tree.column("Token", anchor="center")
token_output_tree.pack(fill="both", expand=True, padx=1, pady=1)

# Process Button
process_button = ttk.Button(root, text="TOKENIZE", command=process_input, style="Custom.TButton")
process_button.grid(row=1, column=1, padx=3, sticky="nsew")

# Error Output Section
error_output_frame = ttk.LabelFrame(root, text="ERROR HANDLING", style="Custom.TLabelframe")
error_output_frame.grid(row=2, column=0, columnspan=2, padx=1, pady=1, sticky="nsew")

error_output_textbox = tk.Text(error_output_frame, wrap=tk.WORD, height=5, state=tk.DISABLED, bg="#534857", fg="#ffffff")
error_output_textbox.pack(fill="both", expand=True, padx=1, pady=1)

# Run the application
root.mainloop()