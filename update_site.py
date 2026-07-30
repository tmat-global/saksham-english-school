import os
import re

lenis_snippet = """
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
    changes_made = []

    # Determine depth relative to root (saksham-english-school)
    # Root index.html depth = 0, subfolders depth = 1 (e.g., contact/index.html)
    rel_path = os.path.relpath(filepath, '.')
    depth = rel_path.count(os.sep)
    prefix = "../" * depth if depth > 0 else ""

    # 1. Add Lenis (if not already present)
    if "lenis.min.js" not in content.lower():
        if "</body>" in content:
            content = content.replace("</body>", lenis_snippet)
            changes_made.append("Added Lenis Smooth Scroll")

    # 2. Update Footer Links in "QUICK LINKS" and "MORE DOCUMENTS"
    # We target sections or lists inside the footer containing these headers
    def replace_footer_links(match):
        header = match.group(1)
        ul_content = match.group(2)
        # Replace href values inside this specific list with prefix + index.html
        updated_ul = re.sub(r'href="[^"]*?"', f'href="{prefix}index.html"', ul_content)
        return header + updated_ul

    # Match common patterns for footer quick links / documents blocks
    pattern = re.sub(
        r'<(h[2-3][^>]*>(?:QUICK LINKS|MORE DOCUMENTS)</h[2-3]>)\s*<ul[^>]*>(.*?)</ul>',
        replace_footer_links,
        content,
        flags=re.IGNORECASE | re.DOTALL
    )
    if pattern != content:
        content = pattern
        changes_made.append(f"Updated Quick Links / More Documents hrefs to use '{prefix}index.html'")

    # 3. Update Registration Office Phone & WhatsApp
    # Replace placeholder or old numbers in Registration Office section
    reg_office_pattern = re.compile(r'(REGISTRATION OFFICE.*?</(?:div|ul|p|address)>)', re.DOTALL | re.IGNORECASE)
    
    def update_reg_office(match):
        block = match.group(1)
        # Check if phone number needs updating
        new_block = re.sub(r'Phone:\s*[\+\d\s\[\]\-]+', 'Phone: <a href="tel:+918551031810">+91 8551031810</a>', block, flags=re.IGNORECASE)
        if new_block == block:
            # Fallback if formatted differently
            new_block = re.sub(r'\+91\s*\[\s*Contact Number\s*\]', '+91 8551031810', block, flags=re.IGNORECASE)
        
        # Add WhatsApp if not present
        if "wa.me/918551031810" not in new_block:
            wa_line = '<br>WhatsApp: <a href="https://wa.me/918551031810" target="_blank">+91 8551031810</a>'
            # Insert near phone or at the end of the block before closing tag
            new_block = re.sub(r'(</(?:p|div|li)>)', wa_line + r'\1', new_block, count=1, flags=re.IGNORECASE)
        return new_block

    updated_content = re.sub(r'(REGISTRATION OFFICE[\s\S]*?</(?:div|ul|p)>)', update_reg_office, content, flags=re.IGNORECASE)
    if updated_content != content:
        content = updated_content
        changes_made.append("Updated Registration Office phone and added WhatsApp contact link")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[UPDATED] {filepath} -> Changes: {', '.join(changes_made)}")
    else:
        print(f"[SKIPPED] {filepath} -> No matching patterns or already updated.")

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
