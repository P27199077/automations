# GitHub Automations

## Scripts

### 1. `make_public.py`
A Python script to bulk update the visibility of multiple private repositories to **Public** using the GitHub REST API.

* **Configuration**:
  - Open `make_public.py` and set your GitHub Personal Access Token in `TOKEN`.
  - Enter your username in `USERNAME`.
  - List the repository names in `REPOS`.
* **Usage**:
  ```bash
  python3 make_public.py
  ```
