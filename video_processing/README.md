# Video Background Removal Automation

A Python script to remove solid color backgrounds (chroma keying) or complex backgrounds (AI subject segmentation) from videos and output transparent video files (`.webm`, `.mov`) or transparent image sequences (`.png`).

---

## 🚀 Setup and Dependencies

This tool requires **FFmpeg** and **FFprobe** installed on your system.

### 1. Install FFmpeg
On macOS, install via Homebrew:
```bash
brew install ffmpeg
```

### 2. Python Packages
Install dependencies listed in the main `requirements.txt`:
```bash
pip install -r ../requirements.txt
```
*Note: If you use the AI method (`-m ai`), the script will automatically check for `rembg` and prompt to install it if missing.*

---

## 📖 Usage Examples

### 1. Chroma Key (Green Screen) to WebM (Default)
Removes the green screen from a video and outputs a transparent WebM video:
```bash
python3 remove_video_bg.py -i input.mp4
```

### 2. AI Segmentation (Complex Backgrounds)
Removes a complex background from a selfie/talking-head video and outputs a transparent WebM:
```bash
python3 remove_video_bg.py -i input.mp4 -m ai
```

### 3. Custom Chroma Key color (e.g., Blue Screen) to QuickTime MOV
Removes a blue background and outputs a transparent ProRes MOV:
```bash
python3 remove_video_bg.py -i input.mp4 -c blue -f mov
```
Other color values supported: `red`, hex codes (`#0000FF`), or comma-separated RGB (`0,0,255`).

### 4. Custom Chroma Key Threshold and Edge Softness
Fine-tune green screen extraction:
```bash
python3 remove_video_bg.py -i input.mp4 -t 45.0 -s 15.0
```
- `-t / --tolerance`: Threshold to match the key color (higher matches more colors).
- `-s / --softness`: Softness of the alpha channel gradient near edges.

---

## 🎛️ Command Line Interface Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `-i / --input` | Path to the input video file (mp4, mov, avi, etc.) | *Prompted* |
| `-o / --output` | Custom destination path for the transparent output | *In-place* |
| `-m / --method` | Removal method: `chroma` (color key) or `ai` (segmentation) | `chroma` |
| `-f / --format` | Output format: `webm` (VP9), `mov` (ProRes), `png` (PNG folder) | `webm` |
| `-c / --color` | Target chroma color to extract (`green`, `blue`, hex, RGB) | `green` |
| `-t / --tolerance` | Chroma color range matching sensitivity | `60.0` |
| `-s / --softness` | Edge softness gradient size for transparency transition | `10.0` |
