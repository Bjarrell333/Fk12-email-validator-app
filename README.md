# Fk12 Email Validator App for Mac

This is a Python-based email validator application designed specifically for macOS. It uses Tkinter to provide a user-friendly GUI for validating email addresses by checking MX records and SMTP responses. The application supports validating single or multiple emails (including CSV file input) and exporting the results to CSV.

## Features

- **Email Validation:**  
  Validates email addresses by checking domain MX records and performing SMTP tests.
- **Multiple Input Options:**  
  Enter one or more email addresses directly, or load them from a CSV file.
- **Results Export:**  
  Export the validation results (email, status, and details) to a CSV file.
- **macOS Optimized:**  
  Uses macOS-friendly assets (e.g., PNG icons) and includes a GitHub Actions workflow to build a standalone executable using PyInstaller.
- **Continuous Integration:**  
  A GitHub Actions workflow builds the app and creates a distributable executable whenever changes are pushed to the `main` branch.

## Prerequisites

- **Python 3.x**  
  Ensure Python is installed on your system.
- **Tkinter**  
  Usually bundled with Python. If missing, install it via your package manager.
- **PyInstaller**  
  Used to build the standalone executable.  
  Install with:
  ```bash
  pip install pyinstaller

