#!/usr/bin/env python3
"""
Script para generar la sección de proyectos en README.md desde info.json
Uso: python generate_readme.py
"""

import json
import re

def load_projects():
    """Carga los proyectos desde info.json"""
    with open('info.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_projects_table(projects):
    """Genera la tabla HTML de proyectos visibles"""
    # Invertir el orden para que los últimos aparezcan primero
    visible_projects = [p for p in projects if p[2] == 1][::-1]
    
    if not visible_projects:
        return ""
    
    # Generar filas de 4 columnas
    rows = []
    for i in range(0, len(visible_projects), 4):
        row_projects = visible_projects[i:i+4]
        cells = []
        
        for project in row_projects:
            image_name, url, _ = project
            name_part = image_name.split('.')[0]
            if '_' in name_part:
                alt_text = name_part.split('_')[1]
            else:
                alt_text = name_part
            
            if url:
                cell = f'<td align="center"><a href="{url}" target="_blank"><img src="images/{image_name}" width="250" alt="{alt_text}" /></a></td>'
            else:
                cell = f'<td align="center"><img src="images/{image_name}" width="250" alt="{alt_text}" /></td>'
            
            cells.append(cell)
        
        # Rellenar con celdas vacías si es necesario
        while len(cells) < 4:
            cells.append('<td></td>')
        
        rows.append('<tr>\n' + '\n'.join(cells) + '\n</tr>')
    
    return '<table>\n' + '\n'.join(rows) + '\n</table>'

def update_readme(table_html):
    """Actualiza la sección de proyectos en README.md y README_EN.md"""
    readme_files = [
        ('README.md', r'(## Proyectos\s*<div align="center">\s*)<table>.*?</table>(\s*</div>)'),
        ('README_EN.md', r'(## Projects\s*<div align="center">\s*)<table>.*?</table>(\s*</div>)')
    ]
    
    for readme_file, pattern in readme_files:
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        replacement = r'\1' + table_html + r'\2'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    print("[OK] README.md y README_EN.md actualizados correctamente")

def main():
    projects = load_projects()
    visible_count = sum(1 for p in projects if p[2] == 1)
    print(f"Proyectos cargados: {len(projects)}")
    print(f"Proyectos visibles: {visible_count}")
    
    table_html = generate_projects_table(projects)
    update_readme(table_html)

if __name__ == '__main__':
    main()
