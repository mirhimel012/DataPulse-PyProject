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


# Function to visualize data with slider 
def visualize_data():
    file_path = csv_file_path.get()
    charts = []

    def create_charts_from_csv(df):
        figs = []

        # Chart 1: Revenue vs Expenses vs Net Profit
        cols = ['Annual Revenue', 'Annual Expenses', 'Net Profit']
        if all(col in df.columns for col in cols):
            fig, ax = plt.subplots(figsize=(6, 4))
            values = df[cols].mean()
            values.plot(kind='bar', ax=ax, color=['#66BB6A', '#EF5350', '#42A5F5'])
            ax.set_title("Revenue vs Expenses vs Net Profit", fontsize=14)
            fig.tight_layout()
            figs.append(fig)

        # Chart 2: Assets vs Liabilities
        cols = ['Total Assets', 'Total Liabilities']
        if all(col in df.columns for col in cols):
            fig, ax = plt.subplots(figsize=(6, 4))
            values = df[cols].mean()
            values.plot(kind='bar', ax=ax, color=['#FFA726', '#AB47BC'])
            ax.set_title("Assets vs Liabilities", fontsize=14)
            fig.tight_layout()
            figs.append(fig)

        # Chart 3: Top 5 KPIs
        kpi_cols = ['Annual Revenue', 'Net Profit (Optional)', 'Market Share Percentage',
                    'Customer Satisfaction Score (out of 100)', 'Number of Active Customers']
        available_kpis = [col for col in kpi_cols if col in df.columns]
        if available_kpis:
            fig, ax = plt.subplots(figsize=(6, 4))
            values = df[available_kpis].mean().sort_values(ascending=False)
            values.plot(kind='bar', ax=ax, color='#29B6F6')
            ax.set_title("Top 5 KPIs", fontsize=14)
            ax.tick_params(axis='x', labelrotation=20)
            fig.tight_layout()
            figs.append(fig)

        # Chart 4: Growth Metrics
        growth_cols = ['Revenue Growth Rate (%)', 'Employee Growth Rate (%)', 'Profit Growth Rate (%)']
        available_growth = [col for col in growth_cols if col in df.columns]
        if available_growth:
            fig, ax = plt.subplots(figsize=(6, 4))
            values = df[available_growth].mean()
            values.plot(kind='bar', ax=ax, color=['#26A69A', '#FFA726', '#AB47BC'])
            ax.set_title("Growth Metrics Comparison", fontsize=14)
            ax.tick_params(axis='x', labelrotation=20)
            fig.tight_layout()
            figs.append(fig)

        # Chart 5: Market Share vs Customer Satisfaction
        if {'Market Share Percentage', 'Customer Satisfaction Score (out of 100)'} <= set(df.columns):
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter(df['Market Share Percentage'], df['Customer Satisfaction Score (out of 100)'], color='#00897B')
            ax.set_xlabel("Market Share (%)")
            ax.set_ylabel("Customer Satisfaction")
            ax.set_title("Market Share vs Customer Satisfaction", fontsize=14)
            fig.tight_layout()
            figs.append(fig)

        # Chart 6: Customers & Product Count
        if {'Number of Active Customers', 'Number of Products/Services'} <= set(df.columns):
            fig, ax = plt.subplots(figsize=(6, 4))
            values = df[['Number of Active Customers', 'Number of Products/Services']].mean()
            values.plot(kind='bar', ax=ax, color=['#FF7043', '#42A5F5'])
            ax.set_title("Customers & Products Count", fontsize=14)
            fig.tight_layout()
            figs.append(fig)

        return figs

    def create_charts_from_manual():
        figs = []

        def get_value(field):
            try:
                val = float(manual_inputs[field].get())
                return val if val != 0 else None
            except:
                return None

        # Common Chart Creator for Bar Charts
        def bar_chart(title, labels, values, colors):
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(labels, values, color=colors)
            ax.set_title(title, fontsize=14)
            ax.tick_params(axis='x', labelrotation=20)
            fig.tight_layout()
            return fig

        # Revenue vs Expenses vs Net Profit
        values = [get_value(f) for f in ['Annual Revenue', 'Annual Expenses', 'Net Profit']]
        if all(v is not None for v in values):
            figs.append(bar_chart("Revenue vs Expenses vs Net Profit", ['Revenue', 'Expenses', 'Net Profit'], values, ['#66BB6A', '#EF5350', '#42A5F5']))

        # Assets vs Liabilities
        values = [get_value(f) for f in ['Total Assets', 'Total Liabilities']]
        if all(v is not None for v in values):
            figs.append(bar_chart("Assets vs Liabilities", ['Assets', 'Liabilities'], values, ['#FFA726', '#AB47BC']))

        # Top 5 KPIs
        kpi_fields = ['Annual Revenue', 'Net Profit (Optional)', 'Market Share Percentage', 'Customer Satisfaction Score (out of 100)', 'Number of Active Customers']
        kpi_data = {f: get_value(f) for f in kpi_fields if get_value(f) is not None}
        if kpi_data:
            figs.append(bar_chart("Top 5 KPIs", list(kpi_data.keys()), list(kpi_data.values()), ['#29B6F6'] * len(kpi_data)))

        # Growth Metrics
        growth_fields = ['Revenue Growth Rate (%)', 'Employee Growth Rate (%)', 'Profit Growth Rate (%)']
        growth_data = {f: get_value(f) for f in growth_fields if get_value(f) is not None}
        if growth_data:
            figs.append(bar_chart("Growth Metrics Comparison", list(growth_data.keys()), list(growth_data.values()),
                                  ['#26A69A', '#FFA726', '#AB47BC']))

        # Market Share vs Customer Satisfaction
        market_share, satisfaction = get_value('Market Share Percentage'), get_value('Customer Satisfaction Score (out of 100)')
        if market_share is not None and satisfaction is not None:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter([market_share], [satisfaction], color='#00897B')
            ax.set_xlabel("Market Share (%)")
            ax.set_ylabel("Customer Satisfaction")
            ax.set_title("Market Share vs Customer Satisfaction", fontsize=14)
            fig.tight_layout()
            figs.append(fig)

        # Customers & Product Count
        values = [get_value(f) for f in ['Number of Active Customers', 'Number of Products/Services']]
        if all(v is not None for v in values):
            figs.append(bar_chart("Customers & Products Count", ['Customers', 'Products'], values, ['#FF7043', '#42A5F5']))

        return figs

    # Load charts from CSV or Manual
    if file_path:
        try:
            df = pd.read_csv(file_path)
            charts = create_charts_from_csv(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize data.\n{str(e)}")
            return
    else:
        charts = create_charts_from_manual()

    if not charts:
        messagebox.showerror("Error", "No charts to display.")
        return


    # Chart Slider Window
    slider_window = tk.Toplevel(root)
    slider_window.title("Data Visualizations")
    slider_window.configure(bg="#1e1e2e")
    slider_window.geometry("700x550")

    # Top Info Display Frame
    info_frame = tk.Frame(slider_window, bg="#1e1e2e")
    info_frame.pack(pady=10)

    # Fetch values for top info
    if file_path:
        company_info = {}
        for field in ['Company Name', 'Industry Type', 'Year Established', 'Headquarters Location']:
            if field in df.columns:
                value = str(df[field].iloc[0])
            else:
                value = "N/A"
            company_info[field] = value
    else:
        company_info = {}
        for field in ['Company Name', 'Industry Type', 'Year Established', 'Headquarters Location']:
            value = manual_inputs[field].get() if field in manual_inputs else "N/A"
            company_info[field] = value if value else "N/A"

    # Display top info labels
    for key, value in company_info.items():
        label = tk.Label(info_frame, text=f"{key}: {value}", font=("Verdana", 12),
                         bg="#1e1e2e", fg="white", anchor="w")
        label.pack(anchor="w")

    current_chart = [0]
    canvas = [None]

    def show_chart(index):
        nonlocal canvas
        if canvas[0]:
            canvas[0].get_tk_widget().destroy()
        fig = charts[index]
        canvas[0] = FigureCanvasTkAgg(fig, master=slider_window)
        canvas[0].draw()
        canvas[0].get_tk_widget().pack(pady=20)

    def next_chart():
        if current_chart[0] < len(charts) - 1:
            plt.close(charts[current_chart[0]])
            current_chart[0] += 1
            show_chart(current_chart[0])

    def prev_chart():
        if current_chart[0] > 0:
            plt.close(charts[current_chart[0]])
            current_chart[0] -= 1
            show_chart(current_chart[0])

    button_frame = tk.Frame(slider_window, bg="#1e1e2e")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="⬅️ Previous", font=("Verdana", 12),
              command=prev_chart).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Next ➡️", font=("Verdana", 12),
              command=next_chart).grid(row=0, column=1, padx=10)

    # Show first chart
    show_chart(0)


# Main window setup
root = tk.Tk()
root.title("Data Pulse – Company Data Analyzer")
root.geometry("800x600")
root.configure(bg="#1e1e2e")

title_label = tk.Label(root, text="📊 Data Pulse 📊", font=("Verdana", 32, "bold"), bg="#1e1e2e", fg="#ffffff")
title_label.pack(pady=30)

sub_label = tk.Label(root, text="Your Smart Company Data Visualizer", font=("Verdana", 14), bg="#1e1e2e", fg="#cccccc")
sub_label.pack(pady=5)

analyze_button = tk.Button(root, text="📊 Analyze Company Data", font=("Verdana", 14),
                           bg="#4CAF50", fg="white", activebackground="#45a049", width=25, height=2, bd=0,
                           command=show_analysis_options, cursor="hand2")
analyze_button.pack(pady=40)

input_frame = tk.Frame(root, bg="#1e1e2e")
manual_inputs = {}

csv_frame = tk.Frame(root, bg="#1e1e2e")
csv_file_path = tk.StringVar()
browse_button = tk.Button(csv_frame, text="📑 Upload CSV", font=("Verdana", 12), command=browse_csv)
file_label = tk.Label(csv_frame, text="No file selected", font=("Verdana", 12), bg="#1e1e2e", fg="white")

analyze_data_button = tk.Button(root, text="📈 Analyze Data", font=("Verdana", 14),
                                bg="#2196F3", fg="white", activebackground="#1976D2",
                                width=20, height=2, bd=0, command=analyze_data, cursor="hand2")

visualize_data_button = tk.Button(root, text="📊 Visualize Data", font=("Verdana", 14),
                                  bg="#FF9800", fg="white", activebackground="#FB8C00",
                                  width=20, height=2, bd=0, command=visualize_data, cursor="hand2")

footer_label = tk.Label(root, text="© 2025 Data Pulse by Himel Mir", font=("Verdana", 10),
                        bg="#1e1e2e", fg="#555555")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
