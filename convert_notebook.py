#!/usr/bin/env python3
"""
Simple script to convert Jupyter notebook (.ipynb) to Python script (.py)
Usage: python3 convert_notebook.py your_notebook.ipynb
"""

import json
import sys
import os

def convert_notebook_to_python(notebook_path):
    """Convert a Jupyter notebook to a Python script"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        python_code = []
        python_code.append("# Converted from Jupyter notebook")
        python_code.append("# Original file: " + os.path.basename(notebook_path))
        python_code.append("")
        
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                if source:
                    # Join source lines and clean up
                    code = ''.join(source)
                    if code.strip():  # Only add non-empty code cells
                        python_code.append(code)
                        python_code.append("")
            elif cell.get('cell_type') == 'markdown':
                # Add markdown as comments
                source = cell.get('source', [])
                if source:
                    markdown = ''.join(source)
                    if markdown.strip():
                        python_code.append("# " + markdown.replace('\n', '\n# '))
                        python_code.append("")
        
        # Write to .py file
        output_path = notebook_path.replace('.ipynb', '.py')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(python_code))
        
        print(f"Converted {notebook_path} to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error converting notebook: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 convert_notebook.py your_notebook.ipynb")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    if not os.path.exists(notebook_path):
        print(f"File not found: {notebook_path}")
        sys.exit(1)
    
    convert_notebook_to_python(notebook_path)