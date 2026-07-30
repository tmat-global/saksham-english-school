import os
import re

lenis_block = """
<!-- Lenis Smooth Scroll Setup -->
<style>
  html.lenis, html.lenis body {
    height: auto;
  }
  .lenis.lenis-smooth {
    scroll-behavior: auto !important;
  }
  .lenis.lenis-smooth [data-lenis-prevent] {
    overscroll-behavior: contain;
  }
  .lenis.lenis-stopped {
    overflow: hidden;
  }
  .lenis.lenis-scrolling iframe {
    pointer-events: none;
  }
</style>
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script>
  const lenis = new Lenis({
    lerp: 0.1,
    wheelMultiplier: 1.0,
    smoothTouch: false,
    infinite: false,
  });
  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);
</script>
</body>"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = []

    # Strip any previous messy or partial lenis scripts/styles to start clean
    content = re.sub(r'<!--\s*Lenis.*?\s*-->.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script src="[^"]*lenis[^"]*"></script>\s*<script>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Insert the complete Lenis block right before </body>
    if "</body>" in content:
        content = content.replace("</body>", lenis_block)
        changes_made.append("Injected optimized Lenis Smooth Scroll CSS & JS configuration")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[UPDATED] {filepath} -> {', '.join(changes_made)}")
    else:
        print(f"[SKIPPED] {filepath}")

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
