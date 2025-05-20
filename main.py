import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to browse CSV file
def browse_csv():
    global csv_file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        csv_file_path.set(file_path)
        file_label.config(text=f"Selected: {file_path.split('/')[-1]}")

# Function to display the Analysis options
def show_analysis_options():
    # Hide main menu widgets
    title_label.pack_forget()
    sub_label.pack_forget()
    analyze_button.pack_forget()
    footer_label.pack_forget()

    # Show Manual Input Section
    input_frame.pack(pady=10)

    fields = [
        "Company Name", "Industry Type", "Year Established", "Headquarters Location",
        "Annual Revenue", "Annual Expenses", "Net Profit", "Total Assets",
        "Total Liabilities", "Number of Employees", "Number of Branches",
        "Number of Products/Services", "Number of Active Customers",
        "Customer Satisfaction Score (out of 100)", "Market Share Percentage",
        "Revenue Growth Rate (%)", "Employee Growth Rate (%)", "Profit Growth Rate (%)"
    ]

    row = 0
    col = 0
    for field in fields:
        label = tk.Label(input_frame, text=field + ":", font=("Verdana", 12), bg="#1e1e2e", fg="white")
        label.grid(row=row, column=col*2, sticky="e", padx=10, pady=5)
        entry = tk.Entry(input_frame, font=("Verdana", 12), width=20)
        entry.grid(row=row, column=col*2 + 1, padx=10, pady=5)
        manual_inputs[field] = entry

        col += 1
        if col >= 2:
            col = 0
            row += 1

    # Show CSV Upload Section
    csv_frame.pack(pady=20)
    browse_button.pack(side="left", padx=5)
    file_label.pack(side="left", padx=5)

    # Show Analyze Data and Visualize Data buttons
    analyze_data_button.pack(pady=20)
    visualize_data_button.pack(pady=10)

# Function to analyze data
def analyze_data():
    file_path = csv_file_path.get()
    if file_path:
        try:
            df = pd.read_csv(file_path)
            total_rows = len(df)
            total_columns = len(df.columns)
            columns_list = df.columns.tolist()
            messagebox.showinfo("CSV Analysis",
                f"✅ CSV File Loaded Successfully!\n\n"
                f"📊 Total Records: {total_rows}\n"
                f"🗂️ Total Columns: {total_columns}\n"
                f"📑 Columns: {', '.join(columns_list)}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file.\n{str(e)}")
    else:
        if not manual_inputs:
            messagebox.showerror("Error", "No manual inputs found.")
            return
        analysis_results = "📋 Manual Input Data Analysis:\n\n"
        for field, entry in manual_inputs.items():
            value = entry.get()
            analysis_results += f"{field}: {value if value else 'N/A'}\n"
        messagebox.showinfo("Manual Data Analysis", analysis_results)

# Main window setup
root = tk.Tk()
root.title("Data Pulse – Company Data Analyzer")
root.geometry("800x600")
root.configure(bg="#1e1e2e")

# UI Elements
title_label = tk.Label(root, text="📊 Data Pulse 📊", font=("Verdana", 32, "bold"), bg="#1e1e2e", fg="#ffffff")
title_label.pack(pady=30)

sub_label = tk.Label(root, text="Your Smart Company Data Visualizer", font=("Verdana", 14), bg="#1e1e2e", fg="#cccccc")
sub_label.pack(pady=5)

analyze_button = tk.Button(root, text="📊 Analyze Company Data", font=("Verdana", 14),
                         bg="#4CAF50", fg="white", activebackground="#45a049", width=25, height=2, bd=0,
                         cursor="hand2")
analyze_button.pack(pady=40)

footer_label = tk.Label(root, text="© 2025 Data Pulse by Himel Mir", font=("Verdana", 10),
                      bg="#1e1e2e", fg="#555555")
footer_label.pack(side="bottom", pady=10)

root.mainloop()