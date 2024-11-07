import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import run_alignments, calculate_percentages, classify_sequences
from utils import load_sequences
import os

class DNASequenceApp:
        def __init__(self, root):
            self.root = root
            self.root.title("DNA Sequence Analyzer")
            self.root.attributes("-fullscreen", True)

            # Main Frame
            self.main_frame = ttk.Frame(root)
            self.main_frame.pack(fill=tk.BOTH, expand=True)

            # Add Logo
            self.logo = tk.PhotoImage(file="logo.png")  # Ensure logo.png is in the same directory
            self.logo_label = ttk.Label(self.main_frame, image=self.logo)
            self.logo_label.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)  # Positioning the logo to the top right

            # Labels
            self.label = ttk.Label(self.main_frame, text="Upload DNA Sequences (FASTA format):", font=("Helvetica", 18, "bold"))
            self.label.pack(pady=(30, 10), anchor="center")

            # Buttons
            self.load_button = ttk.Button(self.main_frame, text="Browse Files", command=self.load_sequences_gui, width=20, style="TButton")
            self.load_button.pack(pady=1, anchor="center")  # Adjusted pady

            self.align_button = ttk.Button(self.main_frame, text="Perform Alignment", state=tk.DISABLED, command=self.perform_alignment, width=20, style="TButton")
            self.align_button.pack(pady=1, anchor="center")  # Adjusted pady

            self.percent_button = ttk.Button(self.main_frame, text="Calculate Percentages", state=tk.DISABLED, command=self.calculate_percentages_gui, width=20, style="TButton")
            self.percent_button.pack(pady=1, anchor="center")  # Adjusted pady

            self.classify_button = ttk.Button(self.main_frame, text="Classify Sequences", state=tk.DISABLED, command=self.classify_sequences_gui, width=20, style="TButton")
            self.classify_button.pack(pady=1, anchor="center")  # Adjusted pady

            self.save_button = ttk.Button(self.main_frame, text="Save Output", state=tk.DISABLED, command=self.save_output_gui, width=20, style="TButton")
            self.save_button.pack(pady=1, anchor="center")  # Adjusted pady

            # Custom threshold input for classification
            self.threshold_label = ttk.Label(self.main_frame, text="Set Classification Threshold (default 900):", font=("Helvetica", 12))
            self.threshold_label.pack(pady=(10, 5), anchor="center")

            self.threshold_entry = ttk.Entry(self.main_frame)
            self.threshold_entry.pack(pady=5, anchor="center")
            self.threshold_entry.insert(0, "900")  # Default value is 900

            # Result label
            self.result_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 16), foreground="green")
            self.result_label.pack(pady=(20, 5), anchor="center")

            # Progress bar for long tasks
            self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
            self.progress.pack(pady=20, anchor="center")

            # Exit button
            self.exit_button = ttk.Button(self.main_frame, text="Exit", command=self.close_fullscreen, width=10, style="TButton")
            self.exit_button.pack(pady=(10, 30), anchor="center")

            # Initialize variables to hold data
            self.sequence_files = []
            self.sequences = []
            self.alignment_scores = []
            self.percentages = []
            self.classifications = []

            # Adding styles
            self.style = ttk.Style()
            self.style.configure("TButton", font=("Helvetica", 14), padding=10)

        def load_sequences_gui(self):
            files = filedialog.askopenfilenames(title="Select DNA Sequences", filetypes=(("FASTA files", "*.fasta"), ("All files", "*.*")))
            if files:
                self.sequence_files = files
                self.sequences = load_sequences(files)
                if len(self.sequences) >= 2:
                    self.align_button.config(state=tk.NORMAL)
                    self.percent_button.config(state=tk.NORMAL)
                    self.classify_button.config(state=tk.NORMAL)
                    self.save_button.config(state=tk.NORMAL)
                    messagebox.showinfo("Files Loaded", f"Loaded {len(files)} DNA sequences successfully.")
                else:
                    messagebox.showerror("Error", "Please select at least two sequences.")
            else:
                messagebox.showerror("Error", "No files selected.")

        def perform_alignment(self):
            if not self.sequences:
                messagebox.showerror("Error", "No sequences loaded.")
                return
            self.progress.start()
            self.alignment_scores = run_alignments(self.sequences)
            self.progress.stop()
            alignment_text = "\n".join([f"{pair}: {score}" for pair, score in self.alignment_scores])
            self.result_label.config(text=f"Alignment Scores:\n{alignment_text}")
            self.show_alignment_histogram()

        def calculate_percentages_gui(self):
            if not self.sequences:
                messagebox.showerror("Error", "No sequences loaded.")
                return
            self.percentages = calculate_percentages(self.sequences)
            percentage_text = "\n".join([f"{seq}: {percentages}" for seq, percentages in self.percentages])
            self.result_label.config(text=f"Percentages:\n{percentage_text}")
            self.show_percentage_chart()

        def classify_sequences_gui(self):
            if not self.alignment_scores:
                messagebox.showerror("Error", "Perform alignments before classification.")
                return
            threshold_value = int(self.threshold_entry.get())
            self.classifications = classify_sequences(self.alignment_scores, threshold=threshold_value)
            classification_text = "\n".join([f"{pair}: {result}" for pair, result in self.classifications])
            self.result_label.config(text=f"Classification Results:\n{classification_text}")

        def save_output_gui(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if not file_path:
                return

            data = {
                'Alignment Scores': [f"{pair}: {score}" for pair, score in self.alignment_scores],
                'Percentages': [f"{seq}: {percentages}" for seq, percentages in self.percentages],
                'Classifications': [f"{pair}: {result}" for pair, result in self.classifications]
            }

            df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Save Successful", f"Results saved to {file_path}")

        def close_fullscreen(self):
            self.root.attributes("-fullscreen", False)
            self.root.quit()

        # Visualization functions
        def show_alignment_histogram(self):
            # Create histogram of alignment scores
            scores = [score for _, score in self.alignment_scores]
            fig, ax = plt.subplots()
            ax.hist(scores, bins=10, edgecolor='black')
            ax.set_title('Alignment Scores Distribution')
            ax.set_xlabel('Scores')
            ax.set_ylabel('Frequency')

            # Display the plot in a new window
            self.show_plot_in_window(fig)

        def show_percentage_chart(self):
            # Create bar chart for nucleotide percentages
            for seq, percentages in self.percentages:
                labels = list(percentages.keys())
                values = list(percentages.values())

                fig, ax = plt.subplots()
                ax.bar(labels, values)
                ax.set_title(f'Nucleotide Percentages for {seq}')
                ax.set_xlabel('Nucleotides')
                ax.set_ylabel('Percentage')

                # Display the plot in a new window
                self.show_plot_in_window(fig)

        def show_plot_in_window(self, fig):
            # Create a new window for displaying the plot
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Graph")
            plot_window.geometry("600x400")

            # Embed the plot in the new window
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Set up the Tkinter GUI
if __name__ == "__main__":
        root = tk.Tk()
        app = DNASequenceApp(root)  
        root.mainloop()