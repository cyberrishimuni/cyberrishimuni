from pathlib import Path
import re

base_dir = Path('.')
index_file = base_dir / 'index.html'
text = index_file.read_text(encoding='utf-8')

nav_match = re.search(r'<!-- cyber-vedic header -->(.*?)</header>', text, re.I|re.S)
footer_match = re.search(r'<!-- footer -->(.*?)</footer>', text, re.I|re.S)
if not nav_match or not footer_match:
    raise SystemExit('Could not find header/footer in index')

nav_snippet = '<!-- Cyber-Vedic Header -->' + nav_match.group(1) + '</header>'
footer_snippet = '<!-- Footer -->' + footer_match.group(1) + '</footer>'

head_block_template = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="{style_path}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{style_path}">'''


def normalize_head(html: str, style_path: str) -> str:
    html = re.sub(r'<link[^>]+https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/6\.4\.0/css/all\.min\.css"[^>]*>\s*', '', html)
    html = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]*>\s*', '', html)
    html = re.sub(r'<link[^>]+style\.css"[^>]*>\s*', '', html)
    html = re.sub(r'</head>', f'    {head_block_template.format(style_path=style_path)}\n</head>', html, flags=re.I)
    return html


def apply_page(file_path: Path):
    html = file_path.read_text(encoding='utf-8')
    rel_base = '' if file_path.parent == base_dir else '../'

    nav_custom = nav_snippet
    nav_custom = nav_custom.replace('href="learn.html"', f'href="{rel_base}learn.html"')
    nav_custom = nav_custom.replace('href="team.html"', f'href="{rel_base}team.html"')
    nav_custom = nav_custom.replace('src="image.jpg"', f'src="{rel_base}image.jpg"')
    nav_custom = nav_custom.replace('href="image.jpg"', f'href="{rel_base}image.jpg"')

    if '<header class="cyber-header">' in html:
        html = re.sub(r'<!-- Cyber-Vedic Header -->.*?</header>', nav_custom, html, flags=re.S)
    else:
        if '<div class="circuit-bg"></div>' in html:
            html = html.replace('<div class="circuit-bg"></div>', '<div class="circuit-bg"></div>\n    ' + nav_custom)
        else:
            html = html.replace('<body>', '<body>\n    ' + nav_custom, 1)

    if '<footer class="footer">' in html:
        html = re.sub(r'<!-- Footer -->.*?</footer>', footer_snippet, html, flags=re.S)
    else:
        html = html.replace('</body>', footer_snippet + '\n</body>')

    html = normalize_head(html, f'{rel_base}style.css')

    file_path.write_text(html, encoding='utf-8')
    print('updated', file_path)

for file_path in sorted(base_dir.rglob('*.html')):
    if file_path.name == 'index.html':
        continue
    apply_page(file_path)

print('All files updated')
