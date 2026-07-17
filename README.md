# Custom Developer Automations & Utility Scripts

A structured collection of developer scripts, converters, and asset processors to speed up work and automate repetitive bulk tasks.

---

## 🛠️ Repository Directory Structure

```
automations/
├── README.md                  # Main developer documentation
├── requirements.txt            # Python dependencies for the scripts
│
├── doc_converters/             # Document conversion utilities
│   ├── README.md
│   └── convert_docx_to_pdf.py # DOCX to PDF converter (via Word macOS automation)
│
├── excel_generation/           # Excel spreadsheets creation
│   ├── README.md
│   └── create_life_reset_excel.py # 60-Day life-reset challenge tracker workbook
│
├── github/                     # GitHub repository management
│   ├── README.md
│   └── make_public.py         # Bulk repository visibility updater (Private -> Public)
│
├── image_processing/           # Asset adjustments & transparent backgrounds
│   ├── README.md
│   ├── make_transparent.py    # Target color transparent rendering
│   └── strip_backgrounds.py   # Multi-file background stripping
│
├── theme_tools/                # Style & color palette swappers
│   ├── README.md
│   ├── color_palette_hex.py   # React/Tailwind project hex re-themer
│   └── color_swap.py          # Tailwind slate -> stone color config converter
│
└── video_processing/           # Video alpha-channel extraction tools
    ├── README.md
    └── remove_video_bg.py     # Video background removal utility (chroma or AI)
```

---

## 🚀 Setup and Dependencies

To run these scripts, set up your Python virtual environment and install the required modules:

```bash
# Navigate to the automations folder
cd /Users/tanishagupta/.gemini/antigravity-ide/scratch/automations

# Activate your virtual environment (if not already active)
source ../venv/bin/bin/activate  # or path to your venv bin/activate

# Install requirements
pip install -r requirements.txt
```

---

## 📄 Featured Utility: `convert_docx_to_pdf.py`

This script uses AppleScript via the native macOS `osascript` terminal engine to automate **Microsoft Word** and export a `.docx` file as a high-fidelity `.pdf` file.

* **Usage**:
  ```bash
  # Convert specifying explicit paths
  python3 doc_converters/convert_docx_to_pdf.py -i /path/to/doc.docx -o /path/to/doc.pdf
  
  # Or run without arguments for interactive prompting
  python3 doc_converters/convert_docx_to_pdf.py
  ```

---

## 📝 Contributions and Maintenance

When adding new scripts:
1. Save the script inside its appropriate directory (e.g. `image_processing/` or `github/`).
2. Add a description in the corresponding folder's `README.md`.
3. Update the global structure tree in this root `README.md`.
