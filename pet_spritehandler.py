# Handles the images given and turn them into individual animation frames in the correct size
import os
from pathlib import Path
from PIL import Image

def resize(in_paths: list, size: tuple, out_folder: tuple) -> tuple:
    out_paths = []

    name, animation = out_folder
    x, y = size
    export_dir = Path(name) / animation
    os.makedirs(str(export_dir), exist_ok=True)

    for i, src in enumerate(in_paths):
        with Image.open(src) as im:
            # If it is a GIF
            if hasattr(im,"n_frames"):
                for f in range(im.n_frames):
                    im.seek(f)
                    frame = im.convert("RGBA")
                    resized = frame.resize((x,y))
                    export_path = export_dir / f"{animation}_{x}x{y}_({f}).png"
                    resized.save(export_path, format="PNG")
                    out_paths.append(str(export_path))
            # Everything else
            else:
                im = im.convert("RGBA")
                resized = im.resize((x,y))
                export_path = export_dir / f"{animation}_{x}x{y}_({i}).png"
                resized.save(export_path, format="PNG")
                out_paths.append(str(export_path))

    return tuple(out_paths)