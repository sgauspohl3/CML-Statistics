# Setup

## Coding quick start

Download Python and VS Code — or use the coding language and IDE of your choice. This class uses VS Code and Python, so examples will be harder to follow. I may publish this website with refactored code one day, but don't expect that anytime soon.

### Installation steps

1. Open the Microsoft Store on your Windows machine.
2. Search for **Python** → click **Get** to install.
3. Search for **Visual Studio Code** → click **Get** to install.

```{image} ../images/microsoft-store.png
:alt: Download Python and VS Code
:width: 700px
:align: center
```

### Further guidance

- [code.visualstudio.com/docs/languages/python](https://code.visualstudio.com/docs/languages/python)
- [code.visualstudio.com/docs/python/python-quick-start](https://code.visualstudio.com/docs/python/python-quick-start)

## VS Code layout

Familiarize yourself with the layout of VS Code:

```{image} ../images/vscode.png
:alt: Visual Studio Code
:width: 700px
:align: center
```

1. **Menu Bar** — top navigation and commands
2. **Tab Bar** — open file tabs at the top of the editor
3. **Side Bar** — file explorer, extensions, source control
4. **Coding Window** — main code editor and viewing area
5. **Panel** — integrated terminal, output, problems

## Loading extensions

Open VS Code → click the Extensions icon (Ctrl + Shift + X).

```{image} ../images/extensions.png
:alt: Extensions Panel
:width: 700px
:align: center
```

### Required extensions

- Python
- Python Environments
- Python Debugger
- Jupyter

### Useful extensions

- Pylance
- Pylint

Then open your project folder: **File → Open Folder…**

## Select Python interpreter

1. Open the Command Palette: **Ctrl + Shift + P**
2. Search for **Python: Select Interpreter** and press Enter.
3. Choose your installed Python version or a virtual environment from the list.

```{tip}
Create a virtual environment (`.venv`) for project-level dependency isolation.
```

```{image} ../images/virtual-environment.png
:alt: Virtual Environment
:width: 700px
:align: center
```


```{image} ../images/interpreter.png
:alt: Select Interpreter
:width: 700px
:align: center
```

## Install required libraries

```{image} ../images/terminal.png
:alt: Using the Terminal
:width: 700px
:align: center
```


Open Terminal in VS Code: **Terminal → New Terminal**. Then:

```bash
pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn
pip install plotnine
pip install scipy
pip install statsmodels
pip install pymc
pip install numpyro
pip install xarray
pip install arviz
pip install bambi
```

## Using Jupyter Notebook in VS Code

Prerequisites: Jupyter extension installed and Python interpreter selected.

1. **Open notebook** — open or create a `.ipynb` file; VS Code opens it in the built-in Notebook Editor.
2. **Select kernel** — click **Select Kernel** (top-right) → choose your Python environment or `.venv`.
3. **Run cells** — click ▶ or press **Shift + Enter** to execute the current cell.
4. **View outputs** — results, plots, and DataFrames display inline beneath each cell.

```{tip}
Use **Ctrl + Shift + P → Jupyter: Create New Jupyter Notebook** to start a blank notebook. Use Run All (double-arrow icon) or **Ctrl + Alt + Enter** to execute the full notebook.
```

## Key Python libraries

### NumPy — the ndarray

A homogeneous, fixed-size N-dimensional array (1D vectors, 2D matrices, or higher). All elements share one dtype, which is what makes operations fast.

- **Vectorized operations & broadcasting** — apply math to whole arrays at once; no loops required.
- **Built-in numerics** — statistics, linear algebra, random sampling, indexing/slicing.

```python
import numpy as np

# Vectorized math
x = np.array([1, 2, 3, 4, 5])
x.mean()        # 3.0
x.std()         # 1.414
(x ** 2).sum() # 55
x + 10          # [11, 12, 13, 14, 15]

# 2D array & slicing
M = np.arange(12).reshape(3, 4)
M.shape         # (3, 4)
M[:, 1]         # col 1
M.sum(axis=0)   # col sums
M[M > 5]        # boolean filter
```

### Pandas — DataFrame & Series

- **DataFrame** — a labeled 2D table (think Excel sheet or SQL table).
- **Series** — a single labeled column.
- Slice by label (`.loc`) or position (`.iloc`), filter with boolean masks, group-and-aggregate, merge tables.
- One-line I/O for CSV, Excel, JSON, SQL, Parquet.

```python
import pandas as pd

df = pd.read_csv('sales.csv')
df.head()
df.describe()

west = df[df['region'] == 'West']
west.groupby('product')['revenue'].sum()

df['margin'] = (df['revenue'] - df['cost']) / df['revenue']
df.pivot_table(index='region', columns='quarter', values='revenue', aggfunc='sum')
```

### Matplotlib — figures and axes

- **Figure** — the whole canvas; holds one or more Axes.
- **Axes** — the actual plot areas. This split is what lets you build multi-panel layouts.
- Every label, tick, color, legend, gridline, and font is tunable.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y, label='sin(x)')
ax.legend()
plt.show()
```


## Resources for this course

All materials are available on the course GitHub repository:

- Example data sets
- Python scripts
- Jupyter notebooks

Ask your instructor for the repository URL.

### Additional references

- VS Code Python Docs — [code.visualstudio.com/docs/languages/python](https://code.visualstudio.com/docs/languages/python)
- VS Code Python Quickstart — [code.visualstudio.com/docs/python/python-quick-start](https://code.visualstudio.com/docs/python/python-quick-start)
