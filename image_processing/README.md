# Image Processing Automations

Utilities for image transparency operations using Python's Pillow library.

## Scripts

### 1. `make_transparent.py`
Converts solid background color (defaulting to white) to fully transparent channels.

* **Usage**:
  Edit the source (`img_path`) and destination (`dest_path`) paths directly in the script, then execute:
  ```bash
  python3 make_transparent.py
  ```

---

### 2. `strip_backgrounds.py`
Strips solid backgrounds across multiple image files in a directory using a threshold comparison.

* **Usage**:
  Edit the target folder and files list in the script, then execute:
  ```bash
  python3 strip_backgrounds.py
  ```
