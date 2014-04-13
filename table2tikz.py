#!/usr/bin/env python
import os.path
import tempfile
import shutil
from optparse import OptionParser
from subprocess import call
from pprint import pprint

header = r'''\begin{tikzpicture}
\draw [thick,step=2] (0,0) grid (18,26);
'''

trail = r'''\end{tikzpicture}'''
cell = r'\node at (%(x).1f,%(y).1f) {\huge{$%(c)s$}};'

latex_header = r'''
\documentclass[a4paper]{article}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[colorinlistoftodos]{todonotes}
\usepackage{graphpap}
\usepackage{tikz}
\usepackage{nopageno}
\usepackage[margin=0.4in]{geometry}
\begin{document}
'''

latex_trail = r'''
\end{document}
'''

def parse_sudoku(p):
    if p.count('|'):
        sep = '|'
    else:
        sep = ' '
    d = [[e for e in line.split(sep) if len(e)>0] for line in p.split('\n')]
    d = [r for r in d if len(r)>0]
    d.reverse()
    return d

def get_tikz_lines(d):
    lines = []
    for j, row in enumerate(d):
        for i, c in enumerate(row):
            x = 2*i + 1
            y = 2*j + 1
            lines.append(cell % locals())
            
    return lines

def get_tikz(d, options):
    tikz_lines = get_tikz_lines(d)
    parts = [header, '\n'.join(tikz_lines),trail]
    s = '\n'.join(parts) + '\n'
    return s
    
def make_pdf(tikz, file_name):
    latex = latex_header + tikz + latex_trail
    tmp_dir = tempfile.mkdtemp()
    base_latex_file = os.path.join(tmp_dir, file_name)
    latex_file = base_latex_file + '.tex'
    f = open(latex_file, 'w')
    f.write(latex)
    f.close()
    call(('pdflatex', latex_file), cwd=tmp_dir)
    shutil.copyfile(base_latex_file + '.pdf', file_name + '.pdf')
    shutil.rmtree(tmp_dir)
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-t', action='store_false', dest='out_tikz',
                      default=True, help='Output tikz file')
    parser.add_option('-p', action='store_true', dest='out_pdf',
                      default=False, help='Output PDF file')
    (options, args) = parser.parse_args()
    
    for file_name in args:
        try:
            f = open(file_name, 'r')
        except IOError:
            print "The file", f, "doesn't exist."
        else:
            p = f.read()
            d = parse_sudoku(p)
            f.close()
            base_name = os.path.splitext(file_name)[0]
            tikz = get_tikz(d, options)
            if options.out_tikz:
                out_tikz_file = base_name + ".tikz"
                f = open(out_tikz_file, 'w')
                f.write(tikz)
                f.close()
                print "New file: ", out_tikz_file
                
            if options.out_pdf:
                make_pdf(tikz, base_name)
