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

%s

\\section{Food}

%s

\\end{document}
"""

colonies_content = ""
if isinstance(data['colonies'], list):
    for idx, colony_data in enumerate(data['colonies']):
        colonies_content += "\\subsection*{Colony %d}\n" % (idx + 1)
        colonies_content += "\\begin{itemize}\n"
        colonies_content += "\\item Amount: %s\n" % colony_data['amount']
        colonies_content += "\\item Size: %s\n" % colony_data['size']
        colonies_content += "\\item Coordinates: %s\n" % colony_data['coordinates']
        colonies_content += "\\item Pheromone Grid: %s\n" % colony_data['pheromone grid']
        colonies_content += "\\item Color: %s\n" % colony_data['color']
        colonies_content += "\\end{itemize}\n"

food_content = ""
if isinstance(data['food'], list):
    for idx, food_data in enumerate(data['food']):
        food_content += "\\subsection*{Food %d}\n" % (idx + 1)
        food_content += "\\begin{itemize}\n"
        food_content += "\\item Amount of food: %s\n" % food_data['amount_of_food']
        food_content += "\\end{itemize}\n"

latex_document = latex_template % (colonies_content, food_content)

path = os.path.join("statistics", time.strftime("%Y-%m-%d_%H-%M-%S"))
os.makedirs(path, exist_ok=True)

with open(os.path.join(path, "statistics.tex"), 'w') as output_file:
    output_file.write(latex_document)

# os.system('pdflatex -output-directory={} {}'.format(path, os.path.join(path, "statistics.tex")))
