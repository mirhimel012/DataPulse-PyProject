import tkinter as tk
from tkinter import filedialog, messagebox

# [Keep all previous code from Part 1]

# Add these variables after root setup
input_frame = tk.Frame(root, bg="#1e1e2e")
manual_inputs = {}

csv_frame = tk.Frame(root, bg="#1e1e2e")
csv_file_path = tk.StringVar()
browse_button = tk.Button(csv_frame, text="📑 Upload CSV", font=("Verdana", 12), command=lambda: None)
file_label = tk.Label(csv_frame, text="No file selected", font=("Verdana", 12), bg="#1e1e2e", fg="white")

analyze_data_button = tk.Button(root, text="📈 Analyze Data", font=("Verdana", 14),
                              bg="#2196F3", fg="white", activebackground="#1976D2",
                              width=20, height=2, bd=0, cursor="hand2")

visualize_data_button = tk.Button(root, text="📊 Visualize Data", font=("Verdana", 14),
                                bg="#FF9800", fg="white", activebackground="#FB8C00",
                                width=20, height=2, bd=0, cursor="hand2")

# Add these functions
def browse_csv():
    global csv_file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        csv_file_path.set(file_path)
        file_label.config(text=f"Selected: {file_path.split('/')[-1]}")

def show_analysis_options():
    title_label.pack_forget()
    sub_label.pack_forget()
    analyze_button.pack_forget()
    footer_label.pack_forget()

    # Show Manual Input Section
    input_frame.pack(pady=10)
    
    # Show CSV Upload Section
    csv_frame.pack(pady=20)
    browse_button.pack(side="left", padx=5)
    file_label.pack(side="left", padx=5)
    
    # Show Analyze Data and Visualize Data buttons
    analyze_data_button.pack(pady=20)
    visualize_data_button.pack(pady=10)

# Connect the buttons
analyze_button.config(command=show_analysis_options)
browse_button.config(command=browse_csv)

root.mainloop()