# Fk12 Email Validator App

This is a Python-based email validator application built with Tkinter. It validates email addresses by checking MX records and performing SMTP tests. The app supports validating single or multiple emails (including CSV file input) and exporting results to CSV.

## Features

- **Email Validation:**  
  Validates email addresses by checking domain MX records and performing SMTP tests.
- **Multiple Input Options:**  
  Enter one or more email addresses directly, or load them from a CSV file.
- **Results Export:**  
  Export the validation results (email, status, and details) to a CSV file.
- **Cross-Platform Support:**  
  Works on Windows, macOS, and Linux with platform-specific optimizations (e.g. icon handling).
- **Continuous Integration & Automated Builds:**  
  GitHub Actions workflows have been created for all three systems (Windows, macOS, and Linux) to automatically build a standalone executable whenever changes are pushed to the repository.

## Prerequisites

- **Python 3.x**  
  Ensure Python is installed on your system.
- **Tkinter**  
  Typically bundled with Python. If missing, install it via your package manager.
- **PyInstaller**  
  Used to build the standalone executable. Install with:
  ```bash
  pip install pyinstaller
  
## Other Dependencies:
- The application also requires:
  - email-validator
  - dnspython
  - tqdm
  - Pillow

## Install them using:
```bash
pip install email-validator dnspython tqdm Pillow
```

## Running the Application

To run the application locally, execute:

```bash
python email_validator_app.py
```

### Building a Standalone Executable

GitHub Actions workflows have been set up to build standalone executables for Windows, macOS, and Linux. These workflows are configured to handle platform-specific settings:

- **Windows**: Uses an ICO file with `iconbitmap` and sets the Application User Model ID.
- **macOS**: Uses PNG files with `iconphoto` (with Pillow auto‑converting the icon for macOS if needed).
- **Linux**: Uses PNG icons with standard settings.

You can find these workflows in the `.github/workflows/` directory. They automatically set up the environment and build the application using PyInstaller with the appropriate settings for each platform.

## Repository Location

**Note**: This repository has moved. Please use the new location:  
[https://github.com/Bjarrell333/Fk12-email-validator-app.git](https://github.com/Bjarrell333/Fk12-email-validator-app.git)

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

