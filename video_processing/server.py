import os
import uuid
import threading
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Ensure the script directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from remove_video_bg import convert_video, parse_color

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Global task state storage
# task_id -> { "filename": str, "status": str, "progress": int, "output_filename": str, "error": str, "config": dict }
tasks = {}

def process_video_task(task_id, input_path, output_path, method, format_type, key_color, tolerance, softness, model_name, alpha_matting):
    tasks[task_id]['status'] = 'processing'
    tasks[task_id]['progress'] = 0
    
    def progress_callback(percentage):
        tasks[task_id]['progress'] = percentage

    try:
        success = convert_video(
            input_path=input_path,
            output_path=output_path,
            method=method,
            format_type=format_type,
            key_color=key_color,
            tolerance=tolerance,
            softness=softness,
            progress_callback=progress_callback,
            model_name=model_name,
            alpha_matting=alpha_matting
        )
        if success:
            tasks[task_id]['status'] = 'completed'
            tasks[task_id]['progress'] = 100
        else:
            tasks[task_id]['status'] = 'failed'
            tasks[task_id]['error'] = "Processing failed."
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    task_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, f"{task_id}_{filename}")
    file.save(input_path)

    tasks[task_id] = {
        "id": task_id,
        "filename": filename,
        "input_path": input_path,
        "status": "queued",
        "progress": 0,
        "output_filename": "",
        "error": None
    }
    return jsonify(tasks[task_id])

@app.route('/process/<task_id>', methods=['POST'])
def process(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.json or {}
    method = data.get('method', 'chroma')
    format_type = data.get('format', 'webm')
    color_str = data.get('color', 'green')
    tolerance = float(data.get('tolerance', 60.0))
    softness = float(data.get('softness', 10.0))
    model_name = data.get('model', 'u2net')
    alpha_matting = bool(data.get('alpha_matting', False))

    try:
        key_color = parse_color(color_str)
    except Exception as e:
        return jsonify({"error": f"Invalid color: {str(e)}"}), 400

    filename_base, _ = os.path.splitext(tasks[task_id]['filename'])
    ext = 'webm' if format_type == 'webm' else ('mov' if format_type == 'mov' else 'zip')
    output_filename = f"{task_id}_{filename_base}_transparent.{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    tasks[task_id]['output_filename'] = output_filename
    tasks[task_id]['config'] = {
        "method": method,
        "format": format_type,
        "color": color_str,
        "tolerance": tolerance,
        "softness": softness,
        "model": model_name,
        "alpha_matting": alpha_matting
    }

    # Start asynchronous processing thread
    thread = threading.Thread(
        target=process_video_task,
        args=(task_id, tasks[task_id]['input_path'], output_path, method, format_type, key_color, tolerance, softness, model_name, alpha_matting)
    )
    thread.start()

    return jsonify(tasks[task_id])

@app.route('/status/<task_id>', methods=['GET'])
def status(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(tasks[task_id])

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(list(tasks.values()))

@app.route('/download/<task_id>', methods=['GET'])
def download(task_id):
    if task_id not in tasks or tasks[task_id]['status'] != 'completed':
        return jsonify({"error": "File not ready or task not found"}), 404
    return send_from_directory(OUTPUT_FOLDER, tasks[task_id]['output_filename'], as_attachment=True)

if __name__ == '__main__':
    print("Starting Video Background Removal Server...")
    print("Navigate to http://localhost:5001 in your browser.")
    app.run(host='0.0.0.0', port=5001, debug=True)
