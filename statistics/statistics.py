import json
import os
import time



def build_pdf():
    with open('statistics/statistics.json', 'r') as json_file:
        data = json.load(json_file)
    
    latex_template = """
    \\documentclass{article}
    \\usepackage{hyperref}
    \\usepackage{tikz}
    \\usepackage{pgfplots}
    \\begin{document}

    \\title{Ant Search Statistics}
    \\author{\\url{https://github.com/heyitsalina/ant_search_algorithm}}
    \\maketitle

    \\section{General Information}

    %s

    \\section{Colonies}

    %s

    \\section{Food}

    %s

    \\section{Obstacles}

    %s

    \\section{Overview}

    \\begin{tikzpicture}
    \\begin{axis}[%s, width=12cm, height=7cm, legend pos=outer north east, legend image post style={scale=0.5}]

    \\addplot[only marks, mark=triangle, mark size=8pt, black] coordinates {
    %s
    };
    \\addlegendentry{Colony}

    \\addplot[only marks, mark=*, mark size=8pt, red] coordinates {
    %s
    };
    \\addlegendentry{Food}

    \\addplot[only marks, mark=square, mark size=8pt, blue] coordinates {
    %s
    };
    \\addlegendentry{Obstacle}

    \\end{axis}
    \\end{tikzpicture}

    \\end{document}
    """

    simulation_content = ""
    simulation_content += "Epochs: %s\\newline\n" % data["simulation"][0]["epochs"]
    simulation_content += "Boundaries: %s\n" % data["simulation"][0]["boundaries"]

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
            colonies_content += "\\item Step Size: %s\n" % colony_data['step size']
            colonies_content += "\\item Amount to Carry: %s\n" % colony_data['amount to carry']
            colonies_content += "\\item Search Radius: %s\n" % colony_data['search radius']
            colonies_content += "\\item Pheromone Influence: %s\n" % colony_data['pheromone influence']
            colonies_content += "\\item Pheromone Reduction: %s\n" % colony_data['pheromone reduction']
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

    obstacle_content = ""
    if isinstance(data['obstacles'], list):
        for idx, obstacle_data in enumerate(data['obstacles']):
            obstacle_content += "\\subsection*{Obstacle %d}\n" % (idx + 1)
            obstacle_content += "\\begin{itemize}\n"
            obstacle_content += "\\item Coordinates: %s\n" % obstacle_data['coordinates']
            obstacle_content += "\\item Size: %s\n" % obstacle_data['size']
            obstacle_content += "\\end{itemize}\n"

    min_x, max_x, min_y, max_y = data["simulation"][0]["boundaries"]
    plot_range = f"xmin={min_x}, xmax={max_x}, ymin={min_y}, ymax={max_y}"

    plot_colony = ""
    plot_food = ""
    plot_obstacle = ""
    
    for colony_data in data['colonies']:
        x, y = colony_data['coordinates']
        plot_colony += f"({x+50},{y+50}) "

    for food_data in data['food']:
        x, y = food_data['coordinates']
        plot_food += f"({x+50},{y+50}) "

    for obstacle_data in data['obstacles']:
        x, y = obstacle_data['coordinates']
        plot_obstacle += f"({x+25},{y+25}) "

    latex_document = latex_template % (simulation_content, colonies_content, food_content, obstacle_content, plot_range, plot_colony, plot_food, plot_obstacle)

    directory = time.strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join("statistics", directory)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "statistics.tex"), 'w') as output_file:
        output_file.write(latex_document)

    os.chdir(path)
    os.system(f"pdflatex statistics.tex")


if  __name__ == "__main__":
    build_pdf()