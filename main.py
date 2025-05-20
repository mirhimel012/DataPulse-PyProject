import tkinter as tk
from tkinter import messagebox

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