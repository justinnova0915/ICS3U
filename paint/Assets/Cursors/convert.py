import os
import glob
from PIL import Image, ImageSequence

def convert_apng_to_frames():
    """
    Finds all .png files (potential APNGs) in the current directory,
    detects if they are animated, and extracts frames into subfolders.
    """
    # APNGs often still use the .png extension
    png_files = glob.glob("*.png")
    
    if not png_files:
        print("No .png files found in the current directory.")
        return

    print(f"Checking {len(png_files)} files for animation...")

    for apng_path in png_files:
        try:
            with Image.open(apng_path) as img:
                # Check if the image is animated
                if not getattr(img, "is_animated", False):
                    continue

                # Create subfolder based on filename
                folder_name = os.path.splitext(apng_path)[0] + "_frames"
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    print(f"\nCreated folder: {folder_name}")
                
                print(f"Extracting APNG: {apng_path}...")

                frame_count = 0
                for frame in ImageSequence.Iterator(img):
                    frame_count += 1
                    
                    # Convert to RGBA to ensure transparency is preserved
                    rgba_frame = frame.convert("RGBA")
                    
                    # Save frame with padded index for easy sorting in Pygame
                    output_filename = f"frame_{frame_count:02d}.png"
                    output_path = os.path.join(folder_name, output_filename)
                    rgba_frame.save(output_path, "PNG")
                
                print(f"  Successfully extracted {frame_count} frames.")

        except Exception as e:
            print(f"Could not process {apng_path}: {e}")

if __name__ == "__main__":
    # Ensure pillow is installed: sudo pacman -S python-pillow
    convert_apng_to_frames()
