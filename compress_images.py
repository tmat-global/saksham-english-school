from pathlib import Path
from PIL import Image

IMG_DIR = Path("assets/images")

count = 0
saved = 0

for img_path in IMG_DIR.rglob("*"):
    if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    try:
        old_size = img_path.stat().st_size

        img = Image.open(img_path)

        # Remove EXIF metadata
        img = img.convert("RGB")

        # Resize if larger than 1920px
        max_size = 1920
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        # Save optimized
        img.save(
            img_path,
            format="JPEG",
            quality=72,
            optimize=True,
            progressive=True
        )

        new_size = img_path.stat().st_size

        print(
            f"{img_path} | "
            f"{old_size/1024/1024:.2f}MB -> "
            f"{new_size/1024/1024:.2f}MB"
        )

        saved += old_size - new_size
        count += 1

    except Exception as e:
        print("Skipped:", img_path, e)

print("\n--------------------------------")
print(f"Images processed : {count}")
print(f"Space saved      : {saved/1024/1024:.2f} MB")
