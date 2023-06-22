# Visualization Trajectories

This repository is created for the BSc Informatica thesis **"Bridging the Information Gap: Enhancing Decision Support through Learning Trajectories"** by *Mariska Spigt*. This project is supervised by Charlotte Gevaert MSc and Dr. Zhiming Zhao.
## Code
This code contains two interactive graphs:
- Sunburst (`sunburst.py`)
- Treemap (`treemap.py`)

When you execute the Python file, it will start a local web server on a specific port. This is port `8050` for `sunburst.py` and port `5081` for `treemap.py`. This can be accessed on http://127.0.0.1:[insert port number]/.

The data that is used is being stored using *Google Sheets*. These files can be found [here (trajectories, courses, keywords)](https://docs.google.com/spreadsheets/d/10UCdVVGtJNmEkLoJGqDAduRmQMAa_Z0sYsEFsKCN5AI/edit?usp=sharing) and [here (descriptions)](https://docs.google.com/spreadsheets/d/1CexXZkL6qVgCB0chLWqKDMA714ocBT3W6G_hmKgu52w/edit?usp=sharing).

**Requirements**
The code uses the following programming language and corresponding libraries:
- [Python](https://www.python.org/)
- [Dash](https://dash.plotly.com/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)

**Experiments**
The `php` file that has been used as a landing page for the experiments can be found in the `experiments/` folder, including the corresponding `css` file and images.
