# PDF Toolkit

PDF Toolkit is a simple, easy-to-use desktop application developed in Python with PyQt5, designed to merge and split PDF files. It provides a user-friendly interface for selecting PDF files to merge into a single document or splitting a PDF into separate pages.

## Features

- **Merge PDFs**: Combine multiple PDF files into a single PDF document.
- **Split PDF**: Separate each page of a PDF file into individual PDF files.
- **Reorder Files**: Before merging, you can reorder the selected PDF files using drag-and-drop.
- **Delete Files**: Remove selected files from the list before merging with the delete key.
- **Customizable Output**: Specify a prefix for the output files generated during the split operation.

## Getting Started
You can try the tool using the already generated .ext file by visiting [Download](https://www.alihayajneh.com/media/11/WebsiteFiles/extended.exe)



### Prerequisites

Ensure you have Python installed on your system. This application has been tested with Python 3.8+. You will also need PyQt5 and PyPDF2 libraries.

### Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/alihayajneh/PDF_TOOLKIT.git
cd pdf-toolkit
```

Install the required Python packages:

```bash
pip install PyQt5 PyPDF2
```

### Running the Application

Navigate to the application's directory and run:

```bash
python extended.py
```

## Generating an Executable File

To distribute this application as a standalone executable, follow these steps:

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Navigate to your project directory and run PyInstaller with the following command:

```bash
pyinstaller --onefile --windowed --icon=ic.ico extended.py
```

- `--onefile` creates a single executable file.
- `--windowed` prevents a console window from appearing when the application runs (useful for GUI applications).
- `--icon=ic.ico` specifies the path to your application's icon file.

3. Find the generated executable in the `dist` directory within your project folder.

## Acknowledgments

- Developed by Dr. Ali Hayajneh.
