# Handles the images given and turn them into individual animation frames in the correct size
import os
from pathlib import Path
from PIL import Image

def resize(in_paths: list, size: tuple, out_folder: tuple) -> tuple:
    out_paths = []

    name, animation = out_folder
    x, y = size
    export_dir = Path("pets")/ name / animation
    os.makedirs(export_dir, exist_ok=True)

    def export(image: Image, n:int):
        frame = image.convert("RGBA")
        resized = frame.resize((x,y))
        export_path = export_dir / f"{animation}_{x}x{y}_({n}).png"
        resized.save(export_path, format="PNG")
        out_paths.append(str(export_path))
        print(export_path)
    
    for i, src in enumerate(in_paths):
        print(i, src)
        with Image.open(src) as im:
            # If it is a GIF
            if hasattr(im, "n_frames") and im.n_frames > 1:
                for f in range(im.n_frames):
                    im.seek(f)
                    export(im, i+f)       
            # Everything else
            else:
                print(f"IT STILL HAS n_frames : {im.n_frames}")
                export(im, i)

    return tuple(out_paths)