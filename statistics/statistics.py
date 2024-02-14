import json
import os
import time


def build_pdf():
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
            colonies_content += "\\item Coordinates: %s\n" % colony_data['coordinates']
            colonies_content += "\\item Pheromone Grid: %s\n" % colony_data['pheromone grid']
            colonies_content += "\\item Color: %s\n" % colony_data['color']
            colonies_content += "\\item Food Count: %s\n" % colony_data['food counter']
            colonies_content += "\\end{itemize}\n"

    food_content = ""
    if isinstance(data['food'], list):
        for idx, food_data in enumerate(data['food']):
            food_content += "\\subsection*{Food %d}\n" % (idx + 1)
            food_content += "\\begin{itemize}\n"
            food_content += "\\item Start amount: %s\n" % food_data['start amount']
            food_content += "\\item Amount of food: %s\n" % food_data['amount of food']
            food_content += "\\item Coordinates: %s\n" % food_data['coordinates']
            food_content += "\\end{itemize}\n"

    latex_document = latex_template % (colonies_content, food_content)

    directory = time.strftime("%Y-%m-%d_%H-%M-%S")

    path = os.path.join("statistics", directory)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, "statistics.tex"), 'w') as output_file:
        output_file.write(latex_document)

    os.chdir("statistics\\" + directory)

    os.system(f"pdflatex statistics.tex")