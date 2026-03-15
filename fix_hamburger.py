from pathlib import Path

base_dir = Path('d:/cyberrishimuni/cyberrishimuni')
files = sorted(base_dir.rglob('*.html'))
print('files', len(files))
for f in files:
    t = f.read_text(encoding='utf-8')
    if '<button class="mobile-toggle"' not in t:
        t = t.replace(
            '<nav class="nav-menu">',
            '<button class="mobile-toggle" aria-label="Toggle Navigation"><span></span><span></span><span></span></button>\n            <nav class="nav-menu">',
            1
        )
    if "document.querySelector('.mobile-toggle')" not in t:
        script = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const toggle = document.querySelector('.mobile-toggle');
        const nav = document.querySelector('.nav-menu');
        if (!toggle || !nav) return;

        toggle.addEventListener('click', function() {
            nav.classList.toggle('active');
            toggle.classList.toggle('open');
        });

        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 900) {
                    nav.classList.remove('active');
                    toggle.classList.remove('open');
                }
            });
        });
    });
    </script>
"""
        t = t.replace('</body>', script + '</body>', 1)
    f.write_text(t, encoding='utf-8')
    print('updated', f.name)
