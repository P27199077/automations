import os
import sys
import argparse

try:
    from docx2pdf import convert
except ImportError:
    print("Error: The 'docx2pdf' package is not installed. Please run:")
    print("  pip install docx2pdf")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Convert a DOCX file to a PDF file on macOS using Microsoft Word.")
    parser.add_argument("-i", "--input", help="Path to the input .docx file")
    parser.add_argument("-o", "--output", help="Path to the output .pdf file (optional)")
    args = parser.parse_args()

    docx_path = args.input
    if not docx_path:
        # Prompt the user interactively if not passed via command line
        docx_path = input("Enter the path to the DOCX file: ").strip()

    # Remove surrounding quotes if dragged-and-dropped in the terminal
    if docx_path.startswith(('"', "'")) and docx_path.endswith(('"', "'")):
        docx_path = docx_path[1:-1]

    if not docx_path:
        print("Error: No input path specified.")
        sys.exit(1)

    docx_path = os.path.abspath(docx_path)
    if not os.path.exists(docx_path):
        print(f"Error: The file '{docx_path}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(docx_path) or not docx_path.endswith('.docx'):
        print(f"Error: The file '{docx_path}' is not a valid .docx file.")
        sys.exit(1)

    # Determine output path if not specified
    pdf_path = args.output
    if not pdf_path:
        pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
    else:
        pdf_path = os.path.abspath(pdf_path)

    print(f"Converting:\n  Input:  {docx_path}\n  Output: {pdf_path}\n")
    
    try:
        convert(docx_path, pdf_path)
        print(f"\n✓ Success: PDF successfully created at '{pdf_path}'!")
    except Exception as e:
        print(f"\n✗ Failed: Conversion failed.\nReason: {str(e)}")
        print("\n[NOTE] On macOS, if you receive a permission error, ensure you grant your Terminal/IDE permission to control Microsoft Word in:")
        print("       System Settings > Privacy & Security > Automation")
        sys.exit(1)

if __name__ == "__main__":
    main()
