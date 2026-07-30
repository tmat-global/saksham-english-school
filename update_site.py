import os
import re

lenis_clean_script = """
<!-- Lenis Smooth Scroll -->
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script>
  const lenis = new Lenis();
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
    changes = []

    # 1. Remove conflicting native CSS smooth scrolling
    content = re.sub(r'html\s*\{\s*scroll-behavior\s*:\s*smooth\s*;?\s*\}', '', content, flags=re.IGNORECASE)
    if content != original_content:
        changes.append("Removed conflicting native scroll-behavior: smooth")

    # 2. Clean up any previous multi-line Lenis blocks or styles
    content = re.sub(r'<!--\s*Lenis.*?\s*-->.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style>\s*html\.lenis[\s\S]*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # 3. Inject clean standard Lenis snippet before </body>
    if "</body>" in content:
        # Remove any trailing </body> if we're replacing it cleanly
        content = content.replace("</body>", "")
        content = content.strip() + "\n" + lenis_clean_script
        changes.append("Injected clean Lenis smooth scroll script")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[CLEANED & FIXED] {filepath} -> {', '.join(changes)}")
    else:
        print(f"[SKIPPED] {filepath}")

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
