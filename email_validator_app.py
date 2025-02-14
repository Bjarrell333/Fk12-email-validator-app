import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import dns.resolver
import socket
import csv
import threading
from email_validator import validate_email, EmailNotValidError
from tqdm import tqdm
from PIL import Image, ImageTk
import sys
import os

# OS-Specific settings for icons and header images
if sys.platform == "win32":
    # Windows: use an ICO file
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        ICON_FILE = os.path.join(base_path, "icon.ico")
        HEADER_FILE = os.path.join(base_path, "header.png")
    else:
        ICON_FILE = "icon.ico"
        HEADER_FILE = "header.png"
elif sys.platform == "darwin":
    # macOS: use a PNG file (with Pillow auto-converting if needed)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        ICON_FILE = os.path.join(base_path, "icon.png")
        HEADER_FILE = os.path.join(base_path, "header.png")
    else:
        ICON_FILE = "icon.png"
        HEADER_FILE = "header.png"
else:
    # Assume Linux: use a PNG file
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        ICON_FILE = os.path.join(base_path, "icon.png")
        HEADER_FILE = os.path.join(base_path, "header.png")
    else:
        ICON_FILE = "icon.png"
        HEADER_FILE = "header.png"


class EmailValidatorApp:
    def __init__(self, root):
        self.root = root
        
        # Windows-specific: Set the Application User Model ID.
        if sys.platform == "win32":
            from ctypes import windll
            windll.shell32.SetCurrentProcessExplicitAppUserModelID("FuelSales.EmailChecker")
        
        self.root.title("FuelSales Email Checker")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 800)  # Set minimum window size

        # Configure grid weight
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Set paths for icon and header images
        self.icon_path = ICON_FILE
        self.header_path = HEADER_FILE

        # Set application icon based on OS
        if sys.platform == "win32":
            # Windows uses iconbitmap with an ICO file
            try:
                self.root.iconbitmap(self.icon_path)
            except Exception as e:
                print("Error loading Windows icon:", e)
        else:
            # macOS and Linux use iconphoto with PNG files
            try:
                icon_image = Image.open(self.icon_path)
                self.icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, self.icon_photo)
            except Exception as e:
                print("Error loading icon:", e)

        # Style configuration
        self.setup_styles()

        # Main frame
        main_frame = ttk.Frame(root, style='Main.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)

        # Header with Logo
        self.create_header(main_frame)

        # Single/Multiple Email Section
        self.create_email_input_section(main_frame)

        # CSV Upload Section with both label and button
        ttk.Label(main_frame, text="Check Multiple Emails", style='Header.TLabel').grid(row=4, column=0, pady=10, sticky="w")
        
        upload_button = tk.Button(
            main_frame,
            text="Upload List (CSV)",
            font=('Helvetica', 11),
            bg='#1C1F2E',
            fg='white',
            pady=10,
            padx=20,
            command=self.upload_csv
        )
        upload_button.grid(row=4, column=1, pady=10, sticky="e")

        # Results Table
        self.create_results_table(main_frame)

        # Export Results Button
        self.create_export_button(main_frame)

        # Bind right-click menu for copy/paste
        self.create_right_click_menu()

    def setup_styles(self):
        self.style = ttk.Style()
        
        # Configure main styles
        self.style.configure('Main.TFrame', background='#1C1F2E')
        self.style.configure('Header.TLabel', 
                           background='#1C1F2E',
                           foreground='white',
                           font=('Helvetica', 16, 'bold'))
        self.style.configure('SubHeader.TLabel',
                           background='#1C1F2E',
                           foreground='#ffffff',
                           font=('Helvetica', 10))
        
        # Custom button style
        self.style.configure('Custom.TButton',
                           background='#1C1F2E',
                           foreground='white',
                           padding=(20, 10),
                           font=('Helvetica', 11))
        
        # Treeview styles
        self.style.configure('Results.Treeview',
                           background='white',
                           fieldbackground='white',
                           rowheight=50,
                           font=('Helvetica', 11))
        self.style.configure('Results.Treeview.Heading',
                           font=('Helvetica', 12, 'bold'))

    def create_header(self, parent):
        try:
            header_image = Image.open(self.header_path)
            header_image = header_image.resize((800, 150), Image.Resampling.LANCZOS)
            self.header_photo = ImageTk.PhotoImage(header_image)
            header_label = ttk.Label(parent, image=self.header_photo, background='#1C1F2E')
            header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        except Exception as e:
            print(f"Error loading header: {e}")
            header_label = ttk.Label(parent, text="Email Validator", style='Header.TLabel')
            header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    def create_email_input_section(self, parent):
        ttk.Label(parent, text="Check Email(s)", style='Header.TLabel').grid(row=1, column=0, pady=(20,5), sticky="w")
        ttk.Label(parent, text="Or enter multiple emails separated by commas", style='SubHeader.TLabel').grid(row=2, column=0, pady=(0,10), sticky="w")

        input_frame = ttk.Frame(parent, style='Main.TFrame')
        input_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        input_frame.grid_columnconfigure(0, weight=1)

        self.email_var = tk.StringVar()
        email_entry = tk.Entry(
            input_frame,
            textvariable=self.email_var,
            font=('Helvetica', 12),
            bg='white',
            fg='black'
        )
        email_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        email_entry.bind('<Return>', lambda e: self.validate_single_email())

        check_button = tk.Button(
            input_frame,
            text="Check Email(s)",
            font=('Helvetica', 11),
            bg='#1C1F2E',
            fg='white',
            pady=10,
            padx=20,
            command=self.validate_single_email
        )
        check_button.grid(row=0, column=1, padx=(0, 10))

        upload_button = tk.Button(
            input_frame,
            text="Upload List (CSV)",
            font=('Helvetica', 11),
            bg='#1C1F2E',
            fg='white',
            pady=10,
            padx=20,
            command=self.upload_csv
        )
        upload_button.grid(row=0, column=2)

    def create_results_table(self, parent):
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame, 
            columns=('Email', 'Status', 'Details'),
            show='headings',
            style='Results.Treeview'
        )
        self.tree.column('Email', width=400, anchor="w")
        self.tree.column('Status', width=200, anchor="center")
        self.tree.column('Details', width=400, anchor="w")
        self.tree.heading('Email', text='Email Address')
        self.tree.heading('Status', text='Result')
        self.tree.heading('Details', text='What This Means')

        self.tree.tag_configure('good', background='#d4edda', foreground='#155724')
        self.tree.tag_configure('warning', background='#fff3cd', foreground='#856404')
        self.tree.tag_configure('error', background='#f8d7da', foreground='#721c24')
        self.tree.tag_configure('retry', background='#cce5ff', foreground='#004085')

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def create_right_click_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selection)
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Control-c>", lambda e: self.copy_selection())

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_selection(self):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        values = item['values']
        copy_text = "\t".join(str(v) for v in values)
        self.root.clipboard_clear()
        self.root.clipboard_append(copy_text)
        self.root.update()

    def create_export_button(self, parent):
        export_button = tk.Button(
            parent,
            text="Export Results",
            font=('Helvetica', 11),
            bg='#1C1F2E',
            fg='white',
            pady=10,
            padx=20,
            command=self.export_results
        )
        export_button.grid(row=6, column=0, columnspan=2, pady=20)

    def validate_email_address(self, email):
        try:
            valid = validate_email(email, check_deliverability=False)
            email = valid.email
            domain = email.split('@')[1]
    
            # Try to resolve MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                mx_record = str(mx_records[0].exchange).rstrip('.')
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                return "Do Not Use", "This email won't work - the domain does not exist or cannot receive emails."
            except dns.resolver.LifetimeTimeout:
                return "Try Again", "DNS lookup took too long. Please try again later."
    
            # Function to check email via SMTP (tries both ports)
            def smtp_check(port):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(20)  # Increased timeout
                        sock.connect((mx_record, port))
                        if sock.recv(1024):
                            sock.send(b'HELO example.com\r\n')
                            if sock.recv(1024):
                                sock.send(f'MAIL FROM: <test@example.com>\r\n'.encode())
                                if sock.recv(1024):
                                    sock.send(f'RCPT TO: <{email}>\r\n'.encode())
                                    response = sock.recv(1024).decode()
                                    if "250" in response:
                                        sock.send(f'RCPT TO: <nonexistent_{email}>\r\n'.encode())
                                        catch_all_response = sock.recv(1024).decode()
                                        if "250" in catch_all_response:
                                            return "Double Check", "This domain accepts all emails, even fake ones. Best to verify with the recipient."
                                        return "Good to Go", "This email is valid."
                                    elif "550" in response:
                                        return "Do Not Use", "This email address does not exist."
                                    else:
                                        return "Double Check", "Unclear response. Try sending a test email."
                except socket.timeout:
                    return None  # Indicate timeout
                except ConnectionRefusedError:
                    return "Double Check", "The email server isn't responding. Try sending a test email."
    
            # Try port 25 first, retry with 587 if it times out
            result = smtp_check(25)
            if result is None:
                result = smtp_check(587)
                if result is None:
                    return "Try Again", "Both port 25 and 587 timed out. Check firewall settings."
    
            return result
    
        except EmailNotValidError:
            return "Do Not Use", "This doesn't look like a real email. Check for typos."


    def validate_single_email(self):
        emails = self.email_var.get().strip()
        if not emails:
            messagebox.showwarning("Reminder", "Please enter at least one email address")
            return
        email_list = [e.strip() for e in emails.split(',') if e.strip()]
        for email in email_list:
            threading.Thread(target=self._validate_and_display, args=(email,)).start()

    def _validate_and_display(self, email):
        status, details = self.validate_email_address(email)
        self.root.after(0, self._update_tree, email, status, details)

    def _update_tree(self, email, status, details):
        if status == "Good to Go":
            tag = 'good'
            status = "✓ " + status
        elif status == "Double Check":
            tag = 'warning'
            status = "? " + status
        elif status == "Try Again":
            tag = 'retry'
            status = "↻ " + status
        else:
            tag = 'error'
            status = "⊘ " + status
        self.tree.insert('', 0, values=(email, status, details), tags=(tag,))

    def upload_csv(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Select CSV File"
        )
        if not filename:
            return
        try:
            threading.Thread(target=self._process_csv, args=(filename,)).start()
        except Exception as e:
            messagebox.showerror("Error", f"Error processing CSV: {str(e)}")

    def _process_csv(self, filename):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                emails = [row[0].strip() for row in reader if row and '@' in row[0]]
                if not emails:
                    self.root.after(0, lambda: messagebox.showwarning(
                        "Warning", "No valid email addresses found in the CSV file."
                    ))
                    return
                for email in emails:
                    status, details = self.validate_email_address(email)
                    self.root.after(0, self._update_tree, email, status, details)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Error reading CSV file: {str(e)}"
            ))

    def export_results(self):
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "No results to export!")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Email", "Status", "Details"])
                for item_id in self.tree.get_children():
                    item = self.tree.item(item_id)
                    writer.writerow(item['values'])
            messagebox.showinfo("Success", "Results exported successfully!")

def main():
    root = tk.Tk()
    app = EmailValidatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
