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

\\section{Colonies}

\\begin{itemize}
%s
\\end{itemize}

\\section{Food}

\\begin{itemize}
%s
\\end{itemize}

\\end{document}
"""

colonies_content = ""
if isinstance(data['colonies'], list):
    for idx, colony_data in enumerate(data['colonies']):
        colonies_content += "\\item Colony %d: Amount - %s, Size - %s, Coordinates - %s, Pheromone Grid - %s, Color - %s\n" % (
            idx + 1, colony_data['amount'], colony_data['size'],
            colony_data['coordinates'], colony_data['pheromone grid'], colony_data['color'])

food_content = ""
if isinstance(data['food'], list):
    for idx, food_data in enumerate(data['food']):
        food_content += "\\item Food %d: Amount - %s\n" % (idx + 1, food_data['amount_of_food'])

latex_document = latex_template % (colonies_content, food_content)

path = os.path.join("statistics", time.strftime("%Y-%m-%d_%H-%M-%S"))
os.makedirs(path, exist_ok=True)

with open(os.path.join(path, "statistics.tex"), 'w') as output_file:
    output_file.write(latex_document)

# os.system('pdflatex -output-directory={} {}'.format(path, os.path.join(path, "statistics.tex")))
