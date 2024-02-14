import json
import os
import time

with open('statistics/statistics.json', 'r') as json_file:
    data = json.load(json_file)

latex_template = """
\\documentclass{article}
\\usepackage{hyperref}
\\begin{document}

\\title{Ant Search Statistics}
\\author{\\url{https://github.com/heyitsalina/ant_search_algorithm}}
\\maketitle

\\section{Data}

\\begin{itemize}
%s
\\end{itemize}

\\end{document}
"""

latex_content = ""
for item in data:
    latex_content += "\\item %s: %s\n" % (item, data[item])

latex_document = latex_template % latex_content

path = os.path.join("statistics", time.strftime("%Y-%m-%d_%H-%M-%S"))
os.mkdir(path)

with open(os.path.join(path, "statistics.tex"), 'w') as output_file:
    output_file.write(latex_document)

# Compile LaTeX document to PDF
os.system('texlive output.tex')