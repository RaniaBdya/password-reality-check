content = open('index.html', 'r', encoding='utf-8').read()

footer = '''    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; font-size: 12px; color: #555; text-align: center; line-height: 1.8;">
      Site réalisé dans le cadre d'un projet de sensibilisation à la cybersécurité.<br>
      Hébergé sur GitHub Pages. Ce site ne collecte aucune donnée.
    </footer>'''

content = content.replace('  <script src="script.js"></script>', footer + '\n  <script src="script.js"></script>')

open('index.html', 'w', encoding='utf-8').write(content)
print('ok')