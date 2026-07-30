from pathlib import Path
import re

files = [
    "index.html",
    "apply-and-enroll/index.html",
    "campus-life/index.html",
    "contact/index.html",
    "gallery/index.html",
    "management/index.html",
    "why-us/index.html"
]

for file in files:
    p = Path(file)
    html = p.read_text(encoding="utf-8")

    # Find every Lenis block
    blocks = list(re.finditer(r'<script>\s*const lenis = new Lenis.*?</script>', html, re.S))

    # Keep only the FIRST configured Lenis block
    if len(blocks) > 1:
        first = blocks[0].group(0)

        # Remove all Lenis blocks
        html = re.sub(r'<script>\s*const lenis = new Lenis.*?</script>', '', html, flags=re.S)

        # Remove standalone Lenis CDN
        html = re.sub(
            r'<script\s+src="https://unpkg\.com/lenis[^"]*"></script>',
            '',
            html,
            flags=re.I
        )

        # Fix wrong closing tags
        html = re.sub(r'</html>\s*</body>', '</body>\n</html>', html, flags=re.S)
        html = re.sub(r'</html>', '', html)

        # Insert the kept Lenis block before </body>
        html = html.replace("</body>", "\n" + first + "\n</body>")

        # Ensure proper ending
        if not html.rstrip().endswith("</html>"):
            html = html.rstrip() + "\n</html>\n"

    p.write_text(html, encoding="utf-8")
    print(f"✔ Fixed {file}")

print("\nDone.")
