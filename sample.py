import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from datetime import datetime, date, time

class DataCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cleaner")

        self.data = None

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.data_frame = tk.Frame(root)
        self.data_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.import_btn = tk.Button(self.main_frame, text="Import Data", command=self.import_data)
        self.import_btn.pack()

        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack()

        self.missing_data_btn = tk.Button(self.options_frame, text="Show Missing Data", command=self.show_missing_data)
        self.missing_data_btn.pack_forget()

        self.datatype_btn = tk.Button(self.options_frame, text="Show Data Types", command=self.show_data_types)
        self.datatype_btn.pack_forget()

        self.dropna_btn = tk.Button(self.options_frame, text="Drop Missing Data", command=self.dropna)
        self.dropna_btn.pack_forget()

        self.fill_mean_btn = tk.Button(self.options_frame, text="Fill Missing Data with Mean", command=self.fill_with_mean)
        self.fill_mean_btn.pack_forget()

        self.fwd_fill_btn = tk.Button(self.options_frame, text="Forward Fill", command=self.forward_fill)
        self.fwd_fill_btn.pack_forget()

        self.bwd_fill_btn = tk.Button(self.options_frame, text="Backward Fill", command=self.backward_fill)
        self.bwd_fill_btn.pack_forget()

        self.export_btn = tk.Button(self.options_frame, text="Export Data", command=self.export_data)
        self.export_btn.pack_forget()

        self.drop_column_btn = tk.Button(self.options_frame, text="Drop Columns", command=self.drop_columns)
        self.drop_column_btn.pack_forget()

        self.set_header_btn = tk.Button(self.options_frame, text="Set Header Row", command=self.set_header_row)
        self.set_header_btn.pack_forget()

        self.delete_row_btn = tk.Button(self.options_frame, text="Delete Selected Rows", command=self.delete_selected_rows)
        self.delete_row_btn.pack_forget()

        self.tree = ttk.Treeview(self.data_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_y = tk.Scrollbar(self.data_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_x = tk.Scrollbar(self.data_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("JSON files", "*.json")])
        if file_path:
            if file_path.endswith('.xlsx'):
                self.data = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                self.data = pd.read_json(file_path)

            self.convert_data_types()  # Convert data types after importing
            messagebox.showinfo("Info", "Data Imported Successfully")
            self.show_data()
            self.show_options()

    def convert_data_types(self):
        # Convert Date and Time columns to datetime type
        if self.data is not None:
            if 'Date' in self.data.columns:
                self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce').dt.date
            if 'Time' in self.data.columns:
                try:
                    self.data['Time'] = pd.to_datetime(self.data['Time'], format='%H:%M:%S', errors='coerce').dt.time
                except ValueError:
                    messagebox.showwarning("Warning", "Error converting 'Time' column to datetime.time")

    def show_data(self):
        if self.data is not None:
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = ["Row"] + list(self.data.columns)
            self.tree["show"] = "headings"

            for column in self.tree["columns"]:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=100, anchor=tk.W)

            for idx, row in self.data.iterrows():
                row_values = [idx + 1] + list(row)
                # Ensure 'Time' column is displayed correctly
                if 'Time' in self.data.columns:
                    time_val = row['Time']
                    if pd.notna(time_val):
                        row_values[self.data.columns.get_loc('Time') + 1] = time_val.strftime('%H:%M:%S')
                self.tree.insert("", "end", values=row_values)

    def show_options(self):
        self.missing_data_btn.pack()
        self.datatype_btn.pack()
        self.dropna_btn.pack()
        self.fill_mean_btn.pack()
        self.fwd_fill_btn.pack()
        self.bwd_fill_btn.pack()
        self.export_btn.pack()
        self.drop_column_btn.pack()
        self.set_header_btn.pack()
        self.delete_row_btn.pack()

    def show_missing_data(self):
        if self.data is not None:
            missing_data = self.data.isnull().sum()
            messagebox.showinfo("Missing Data", str(missing_data))
        else:
            messagebox.showwarning("Warning", "No data imported")

    def show_data_types(self):
        if self.data is not None:
            dtype_window = tk.Toplevel(self.root)
            dtype_window.title("Data Types")

            tk.Label(dtype_window, text="Column").grid(row=0, column=0)
            tk.Label(dtype_window, text="Current Data Type").grid(row=0, column=1)
            tk.Label(dtype_window, text="New Data Type").grid(row=0, column=2)

            self.dtype_vars = {}
            for idx, column in enumerate(self.data.columns):
                tk.Label(dtype_window, text=column).grid(row=idx + 1, column=0)
                tk.Label(dtype_window, text=str(self.data[column].dtype)).grid(row=idx + 1, column=1)
                
                dtype_var = tk.StringVar()
                dtype_var.set(str(self.data[column].dtype))
                self.dtype_vars[column] = dtype_var

                dtype_menu = ttk.Combobox(dtype_window, textvariable=dtype_var, values=["int", "float", "str", "date", "time", "datetime"])
                dtype_menu.grid(row=idx + 1, column=2)

            apply_btn = tk.Button(dtype_window, text="Apply Changes", command=lambda: self.apply_data_type_changes(dtype_window))
            apply_btn.grid(row=len(self.data.columns) + 1, column=1, columnspan=2)

        else:
            messagebox.showwarning("Warning", "No data imported")

    def apply_data_type_changes(self, dtype_window):
        if self.data is not None:
            for column, dtype_var in self.dtype_vars.items():
                new_dtype = dtype_var.get()
                if new_dtype != str(self.data[column].dtype):
                    try:
                        if new_dtype == 'int':
                            self.data[column] = self.data[column].astype(int)
                        elif new_dtype == 'float':
                            self.data[column] = self.data[column].astype(float)
                        elif new_dtype == 'str':
                            self.data[column] = self.data[column].astype(str)
                        elif new_dtype == 'date':
                            self.data[column] = pd.to_datetime(self.data[column]).dt.date
                        elif new_dtype == 'time':
                            self.data[column] = pd.to_datetime(self.data[column], format='%H:%M:%S', errors='coerce').dt.time
                        elif new_dtype == 'datetime':
                            self.data[column] = pd.to_datetime(self.data[column])
                        else:
                            messagebox.showerror("Error", f"Invalid data type for column '{column}'")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error converting column '{column}' to {new_dtype}: {e}")
            self.show_data()
            messagebox.showinfo("Info", "Data type changes applied successfully")
            dtype_window.destroy()  # Close the data types window after applying changes
        else:
            messagebox.showwarning("Warning", "No data imported")

    def dropna(self):
        if self.data is not None:
            self.data = self.data.dropna()
            messagebox.showinfo("Info", "Missing data dropped")
            self.show_data()
        else:
            messagebox.showwarning("Warning", "No data imported")

    def fill_with_mean(self):
        if self.data is not None:
            self.data = self.data.fillna(self.data.mean())
            messagebox.showinfo("Info", "Missing data filled with mean")
            self.show_data()
        else:
            messagebox.showwarning("Warning", "No data imported")

    def forward_fill(self):
        if self.data is not None:
            self.data = self.data.fillna(method='ffill')
            messagebox.showinfo("Info", "Missing data forward filled")
            self.show_data()
        else:
            messagebox.showwarning("Warning", "No data imported")

    def backward_fill(self):
        if self.data is not None:
            self.data = self.data.fillna(method='bfill')
            messagebox.showinfo("Info", "Missing data backward filled")
            self.show_data()
        else:
            messagebox.showwarning("Warning", "No data imported")

    def export_data(self):
        if self.data is not None:
            export_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
            if export_path:
                if export_path.endswith('.xlsx'):
                    self.data.to_excel(export_path, index=False)
                elif export_path.endswith('.csv'):
                    self.data.to_csv(export_path, index=False)
                messagebox.showinfo("Info", "Data exported successfully")
        else:
            messagebox.showwarning("Warning", "No data to export")

    def drop_columns(self):
        if self.data is not None:
            drop_window = tk.Toplevel(self.root)
            drop_window.title("Drop Columns")

            tk.Label(drop_window, text="Select columns to drop:").pack()

            self.drop_vars = {}
            for column in self.data.columns:
                var = tk.IntVar()
                self.drop_vars[column] = var
                tk.Checkbutton(drop_window, text=column, variable=var).pack()

            apply_btn = tk.Button(drop_window, text="Apply Drop", command=lambda: self.apply_drop_columns(drop_window))
            apply_btn.pack()

    def apply_drop_columns(self, drop_window):
        if self.data is not None:
            columns_to_drop = [col for col, var in self.drop_vars.items() if var.get() == 1]
            if columns_to_drop:
                self.data.drop(columns=columns_to_drop, inplace=True)
                self.show_data()
                messagebox.showinfo("Info", "Columns dropped successfully")
            else:
                messagebox.showwarning("Warning", "No columns selected to drop")
            drop_window.destroy()  # Close the drop columns window after applying changes
        else:
            messagebox.showwarning("Warning", "No data imported")

    def set_header_row(self):
        if self.data is not None:
            row_number = simpledialog.askinteger("Set Header Row", "Enter the row number to set as header (1-indexed):")
            if row_number is not None and row_number > 0:
                try:
                    self.data.columns = self.data.iloc[row_number - 1]
                    self.data = self.data[1:]
                    self.data.reset_index(drop=True, inplace=True)
                    self.data.columns.name = None
                    messagebox.showinfo("Info", "Header row set successfully")
                    self.show_data()
                except Exception as e:
                    messagebox.showerror("Error", f"Error setting header row: {e}")
            else:
                messagebox.showwarning("Warning", "Invalid row number")
        else:
            messagebox.showwarning("Warning", "No data imported")

    def delete_selected_rows(self):
        selected_items = self.tree.selection()
        if selected_items:
            indices_to_drop = [self.tree.index(item) for item in selected_items]
            self.data.drop(indices_to_drop, inplace=True)
            self.data.reset_index(drop=True, inplace=True)
            self.show_data()
            messagebox.showinfo("Info", "Selected rows deleted successfully")
        else:
            messagebox.showwarning("Warning", "No rows selected to delete")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataCleanerApp(root)
    root.mainloop()
