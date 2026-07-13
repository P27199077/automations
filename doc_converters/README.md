# Document Converters

A collection of tools to convert files between different formats (Markdown to DOCX, DOCX to PDF).

## Scripts

### 1. `convert_docx_to_pdf.py` (New!)
Converts Microsoft Word `.docx` documents to Adobe PDF `.pdf` documents using Microsoft Word automation on macOS. This ensures 100% visual fidelity.

* **Usage**:
  ```bash
  # Convert using CLI arguments:
  python3 convert_docx_to_pdf.py -i /path/to/file.docx -o /path/to/output.pdf
  
  # Or run interactively (it will prompt for the path):
  python3 convert_docx_to_pdf.py
  ```
