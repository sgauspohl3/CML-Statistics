# Setup

## Coding quick start

Download Python and VS Code — or use the coding language and IDE of your choice. This class uses VS Code and Python, so examples will be harder to follow. I may publish this website with refactored code one day, but don't expect that anytime soon.

### Installation steps

1. Open the Microsoft Store on your Windows machine.
2. Search for **Python** → click **Get** to install.
3. Search for **Visual Studio Code** → click **Get** to install.

```{figure} ../images/microsoft-store.png
:name: microsoft-store
:alt: Download Python and VS Code
:width: 700px
:align: center

Screenshots of download screen from Microsoft Store. It says "E for Everyone", but I don't think Python is really for everyone.
```


## VS Code layout

Familiarize yourself with the layout of VS Code:

```{figure} ../images/vscode.png
:name: vscodelayout
:alt: Visual Studio Code
:width: 700px
:align: center

Layout of VS Code
```

<br><br>

1. **Menu Bar** — top navigation and commands
2. **Tab Bar** — open file tabs at the top of the editor
3. **Side Bar** — file explorer, extensions, source control
4. **Coding Window** — main code editor and viewing area
5. **Panel** — integrated terminal, output, problems

## Loading Extensions

Open VS Code → click the Extensions icon (Ctrl + Shift + X).

```{figure} ../images/extensions.png
:name: extensions
:alt: Extensions Panel
:width: 400px
:align: center

Get extensions from the circled icon in the Side Bar
```

### Required Extensions

- Python
- Python Environments
- Python Debugger
- Jupyter

### Useful Extensions

- Pylance
- Pylint


## Open Project Folder

You may want to create a folder for this project. If you work within a folder, you do not need to create absolute paths for files, and you will easily just be able to put files in the folder for your code to use, and any files you create can be downloaded into this folder as well. 

Then open your project folder: **File → Open Folder…**

```{figure} ../images/openfolder.png
:name: openfolder
:alt: Open Folder
:width: 400px
:align: center

Get extensions from the circled icon in the Side Bar
```

## Select Python interpreter

1. Open the Command Palette: **Ctrl + Shift + P**
2. Search for **Python: Select Interpreter** and press Enter.
3. Choose your installed Python version or a virtual environment from the list.

```{tip}
Create a virtual environment (`.venv`) for project-level dependency isolation.
```

```{figure} ../images/virtual-environment.png
:name: virtual-environment
:alt: Virtual Environment
:width: 700px
:align: center
```
<br><br>

```{figure} ../images/interpreter.png
:name: interpreter
:alt: Select Interpreter
:width: 700px
:align: center
```

## Install required libraries

```{figure} ../images/terminal.png
:name: terminal
:alt: Using the Terminal
:width: 400px
:align: center

Copy the code below into your terminal to install all the libraries used in this course
```
<br><br>

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

```{figure} ../images/jupyter.png
:name: jupyter
:alt: Jupyter
:width: 400px
:align: center

Jupyter notebooks are easy to use when trying to analyze data
```

## Key Python libraries

### NumPy

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

Try the following in Pandas by downloading the file and placing in your project folder:
[sales.csv](../_static/data/sales.csv)

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

```
Quarter    Q1        Q2        Q3        Q4
Region
East      928.26   1054.39   1056.08   1142.29
North     907.46   1136.85   1293.83   1415.43
South     757.57   1134.60   1703.73   1268.56
West     1207.81    690.77   1621.47    940.46
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
<br><br>

```{figure} ../images/matplotlib-example1.png
:name: matplotlib-example1
:alt: matplotlib-example1
:width: 400px
:align: center

Your very first plot!
```

<br><br>

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 1, figsize=(3, 6))
np.random.seed(42)
data = np.random.normal(loc=1, scale=7, size=50)
axes[0].hist(data, bins=30)
axes[0].set_title('Histogram')
axes[1].scatter(x, y, alpha=0.5, c='teal')
axes[1].set_title('Scatter')
fig.show()
```
<br><br>

```{figure} ../images/matplotlib-example2.png
:name: matplotlib-example2
:alt: matplotlib-example2
:width: 200px
:align: center

Your very second plot!
```

## A Note on Software Usage

Statistical analysis is typically performed with the assistance of software such as Microsoft Excel, Python, R, MATLAB, Minitab, or other commercial tools. However, different tools may produce different answers, despite a common set of data. Different answers do not necessarily mean one is correct and the other is incorrect. Both answers are technically correct, but understanding how software arrives at an answer is prerequisite to defending that number in an integrity decision. 
Some common examples of software dependent variation are listed below:

-	**Sample Statistics**: Sample standard deviation does not always have the same divisor. In Python, the NumPy library std() command uses n (population form) by default, whereas the Pandas library std() uses n-1 (Bessel corrected sample form). Microsoft Excel’s STDEV.S also uses n-1. For large sample sizes, the difference is negligible, but the effect grows with decreasing sample size.
-	**Plotting Positions and Probability Plots**: Empirical cumulative probability assigned to the ith order statistic varies by convention. In Python, the SciPy library probplot() function calculates plotting positions using the formula (i-0.4)/(n-0.2) (Cunnane) by default, though the method can be programmed to the user’s choice. Minitab calculates plotting positions using the formula (i-0.3)/(n+0.4) (Bernard) by default. While Minitab has some flexibility in plotting positions, the formulas are limited to Bernard, Herd-Johnson, and Kaplan-Meir only. If utilizing the empirical cumulative density function to estimate parameters, the choice of plotting positions will carry through to any calculation utilizing those estimated parameters.   
-	**Distribution Parametrizations**: Distributions may be parametrized differently when using different software packages. In Python, the SciPy library parametrizes a gamma distribution with the shape and scale parameters, whereas in the Python library PyMC (for Bayesian analysis), the gamma distribution is parametrized as shape and rate (rate = 1/scale). 
-	**Optimization Convergence**: Maximum Likelihood Estimation (MLE) for distributions that cannot be solved analytically, such as Weibull, Gumbel, and Gamma) require numerical methods. Different software may have different optimization algorithms, solver tolerances, and default starting values, which can converge to different local maxima.    
-	**Confidence Intervals**: Most software packaged utilize Wald intervals when calculating a confidence interval. However, they do differ slightly in their methods of calculation. In the R library fitdistrplus, confidence intervals are calculated using a Hessian matrix (second-order derivatives of optimizer) formulated with a numerical solution. MATLAB uses a Hessian matrix calculated analytically. While generally negligible in different, these do produce differing values. Packages for specific applications such as in the R library extRemes utilize the profile likelihood method of calculating confidence intervals, whereas in the Python library SciPy does not provide a confidence interval by default.    



### Additional references

- VS Code Python Docs — [code.visualstudio.com/docs/languages/python](https://code.visualstudio.com/docs/languages/python)
- VS Code Python Quickstart — [code.visualstudio.com/docs/python/python-quick-start](https://code.visualstudio.com/docs/python/python-quick-start)
