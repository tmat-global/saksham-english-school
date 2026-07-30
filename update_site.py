import os
import re

lenis_snippet = """
<!-- Lenis Smooth Scroll Fix -->
<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script>
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothTouch: false
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

    # Determine depth relative to root (saksham-english-school)
    rel_path = os.path.relpath(filepath, '.')
    depth = rel_path.count(os.sep)
    prefix = "../" * depth if depth > 0 else ""

    # 1. Clean up any existing Lenis script variations first to avoid duplication/conflicts
    content = re.sub(r'<!--\s*(?:Lenis.*?)?-->\s*<script src="[^"]*lenis[^"]*"></script>\s*<script>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Add the robust Lenis snippet right before </body>
    if "</body>" in content:
        content = content.replace("</body>", lenis_snippet)
        changes_made.append("Updated Lenis Smooth Scroll Configuration")

    # 2. Update Footer Links specifically inside "QUICK LINKS" and "MORE DOCUMENTS" sections
    def replace_links_in_section(match):
        header_tag = match.group(1)
        ul_content = match.group(2)
        # Rewrite every href inside this ul list to point to index.html with correct relative path
        updated_ul = re.sub(r'href="[^"]*?"', f'href="{prefix}index.html"', ul_content)
        return header_tag + updated_ul

    # Match h2/h3/h4/h5 containing QUICK LINKS or MORE DOCUMENTS followed by a list
    pattern = re.compile(r'(<(?:h[2-5])[^>]*>\s*(?:QUICK LINKS|MORE DOCUMENTS)\s*</(?:h[2-5])>)\s*(<ul[^>]*>.*?</ul>)', re.DOTALL | re.IGNORECASE)
    
    new_content = pattern.sub(replace_links_in_section, content)
    if new_content != content:
        content = new_content
        changes_made.append(f"Redirected Quick Links & More Documents to {prefix}index.html")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[UPDATED] {filepath} -> {', '.join(changes_made)}")
    else:
        print(f"[SKIPPED] {filepath} -> No changes needed.")

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
