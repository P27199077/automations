import os
import sys
import shutil
import subprocess
import tempfile
import argparse
from PIL import Image

def get_video_fps(video_path):
    cmd = [
        "ffprobe", 
        "-v", "0", 
        "-of", "csv=p=0", 
        "-select_streams", "v:0", 
        "-show_entries", "stream=r_frame_rate", 
        video_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        rate = result.stdout.strip()
        if "/" in rate:
            num, den = map(float, rate.split("/"))
            return num / den
        return float(rate)
    except Exception:
        return 30.0

def check_dependencies(method):
    # Verify ffmpeg and ffprobe are available
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("Error: 'ffmpeg' and 'ffprobe' must be installed on your system.")
        print("Install via Homebrew: brew install ffmpeg")
        sys.exit(1)

    if method == "ai":
        try:
            import rembg
        except ImportError:
            print("The AI method requires the 'rembg' library.")
            choice = input("Would you like to install 'rembg' now? (y/n): ").strip().lower()
            if choice == 'y':
                print("Installing rembg... (This can take a few minutes)")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "rembg"], check=True)
                    print("rembg successfully installed!")
                except Exception as e:
                    print(f"Failed to install rembg: {str(e)}")
                    sys.exit(1)
            else:
                print("AI method aborted because 'rembg' is not installed.")
                sys.exit(1)

def chroma_key_pixel_data(img, key_color, tolerance, softness):
    img = img.convert("RGBA")
    datas = img.getdata()
    
    newData = []
    kr, kg, kb = key_color
    
    for item in datas:
        r, g, b, a = item
        # Euclidean distance in RGB space
        dist = ((r - kr)**2 + (g - kg)**2 + (b - kb)**2)**0.5
        
        if dist < tolerance:
            newData.append((r, g, b, 0))
        elif dist < tolerance + softness:
            # Soft transition interpolation
            factor = (dist - tolerance) / softness
            alpha = int(255 * factor)
            newData.append((r, g, b, alpha))
        else:
            newData.append(item)
            
    img.putdata(newData)
    return img

def process_frames(temp_in, temp_out, method, key_color, tolerance, softness, progress_callback=None):
    frames = sorted([f for f in os.listdir(temp_in) if f.endswith(".png")])
    if not frames:
        print("Error: No frames found for processing.")
        return False

    try:
        from tqdm import tqdm
    except ImportError:
        # Fallback if tqdm is missing
        def tqdm(iterable, **kwargs):
            return iterable

    print(f"Processing {len(frames)} frames...")
    
    if method == "ai":
        from rembg import remove
        for idx, frame in enumerate(tqdm(frames, desc="AI Segmenting")):
            in_path = os.path.join(temp_in, frame)
            out_path = os.path.join(temp_out, frame)
            with Image.open(in_path) as img:
                res = remove(img)
                res.save(out_path)
            if progress_callback:
                progress_callback(int((idx + 1) / len(frames) * 100))
    else:
        for idx, frame in enumerate(tqdm(frames, desc="Chroma Keying")):
            in_path = os.path.join(temp_in, frame)
            out_path = os.path.join(temp_out, frame)
            with Image.open(in_path) as img:
                res = chroma_key_pixel_data(img, key_color, tolerance, softness)
                res.save(out_path)
            if progress_callback:
                progress_callback(int((idx + 1) / len(frames) * 100))
    return True

def convert_video(input_path, output_path, method, format_type, key_color, tolerance, softness, progress_callback=None):
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    
    check_dependencies(method)
    fps = get_video_fps(input_path)
    print(f"Video Frame Rate: {fps} FPS")

    # Set up temporary directories
    temp_dir = tempfile.mkdtemp(prefix="video_bg_")
    temp_in = os.path.join(temp_dir, "in")
    temp_out = os.path.join(temp_dir, "out")
    os.makedirs(temp_in)
    os.makedirs(temp_out)

    try:
        # 1. Extract frames from input video
        print("Extracting video frames...")
        extract_cmd = [
            "ffmpeg", "-y", "-i", input_path,
            os.path.join(temp_in, "frame_%05d.png")
        ]
        subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # 2. Process each frame
        success = process_frames(temp_in, temp_out, method, key_color, tolerance, softness, progress_callback)
        if not success:
            return False

        # 3. Compile processed frames back to video/sequence
        print("Assembling frames into final output...")
        if format_type == "webm":
            # WebM VP9 supports transparency
            compile_cmd = [
                "ffmpeg", "-y", "-f", "image2", "-framerate", str(fps),
                "-i", os.path.join(temp_out, "frame_%05d.png"),
                "-i", input_path, "-map", "0:v", "-map", "1:a?",
                "-c:v", "libvpx-vp9", "-b:v", "2M", "-pix_fmt", "yuva420p",
                "-c:a", "libopus", "-shortest", output_path
            ]
            subprocess.run(compile_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        elif format_type == "mov":
            # QuickTime Animation supports transparency
            compile_cmd = [
                "ffmpeg", "-y", "-f", "image2", "-framerate", str(fps),
                "-i", os.path.join(temp_out, "frame_%05d.png"),
                "-i", input_path, "-map", "0:v", "-map", "1:a?",
                "-c:v", "qtrle", "-pix_fmt", "argb",
                "-c:a", "copy", "-shortest", output_path
            ]
            subprocess.run(compile_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        elif format_type == "png":
            # Copy output PNG folder to destination
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
            shutil.copytree(temp_out, output_path)
            print(f"PNG sequence saved to: {output_path}")

        print(f"\n✓ Done! Output saved to: {output_path}")
        return True
    finally:
        # Clean up temp files
        shutil.rmtree(temp_dir)

def parse_color(color_str):
    color_str = color_str.strip().lower()
    if color_str == "green":
        return (0, 255, 0)
    elif color_str == "blue":
        return (0, 0, 255)
    elif color_str == "red":
        return (255, 0, 0)
    elif color_str.startswith("#"):
        hex_val = color_str.lstrip('#')
        return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))
    else:
        # Try parsing comma-separated RGB values
        try:
            return tuple(map(int, color_str.split(",")))
        except Exception:
            raise argparse.ArgumentTypeError("Color must be 'green', 'blue', 'red', a hex value (e.g. '#00FF00'), or comma-separated RGB (e.g. '0,255,0')")

def main():
    parser = argparse.ArgumentParser(description="Remove background from video and make it transparent.")
    parser.add_argument("-i", "--input", help="Path to input video file")
    parser.add_argument("-o", "--output", help="Path to output file or folder")
    parser.add_argument("-m", "--method", choices=["chroma", "ai"], default="chroma", help="Background removal method (chroma key vs AI segmentation)")
    parser.add_argument("-f", "--format", choices=["webm", "mov", "png"], default="webm", help="Output transparent format (webm, mov, or png sequence)")
    parser.add_argument("-c", "--color", type=parse_color, default="green", help="Chroma key color to remove (name, hex, or RGB comma-separated)")
    parser.add_argument("-t", "--tolerance", type=float, default=60.0, help="Chroma key tolerance threshold")
    parser.add_argument("-s", "--softness", type=float, default=10.0, help="Chroma key edge softness range")
    
    args = parser.parse_args()

    input_path = args.input
    if not input_path:
        input_path = input("Enter path to input video: ").strip()
    if input_path.startswith(('"', "'")) and input_path.endswith(('"', "'")):
        input_path = input_path[1:-1]

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    # Determine default output path
    output_path = args.output
    if not output_path:
        base, _ = os.path.splitext(input_path)
        if args.format == "png":
            output_path = base + "_frames"
        else:
            output_path = base + "_transparent." + args.format

    convert_video(input_path, output_path, args.method, args.format, args.color, args.tolerance, args.softness)

if __name__ == "__main__":
    main()
