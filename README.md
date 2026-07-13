# Custom Automation Scripts

A collection of utility and automation scripts to speed up developer workflows and perform bulk tasks.

---

## 🛠️ Scripts Directory

### 1. `make_public.py`
A Python automation script that uses the GitHub REST API to bulk update the visibility of multiple private repositories to **Public** in a single run.

* **Configuration**:
  * Set your GitHub Personal Access Token in the `TOKEN` variable.
  * Enter your username in the `USERNAME` variable.
  * List the names of the repositories you want to make public in the `REPOS` array.
* **Usage**:
  ```bash
  python3 make_public.py
  ```

---

## 🚀 Adding New Automations in the Future

When you write a new script (e.g. `cleanup_temp.py`), you can add it to this repository:

1. Save the script inside this folder.
2. Edit this `README.md` to add a description under the directory list.
3. Push the new file to GitHub:
   ```bash
   git add .
   git commit -m "Add script: [Name of your new script]"
   git push origin main
   ```
