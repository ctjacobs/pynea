# Pynea

Pynea facilitates the reproducibility of [LaTeX](https://www.latex-project.org/) documents by embedding the scripts and data files required to regenerate the figures within the document itself. If the scripts and data are stored under Git version control, then the figures are only regenerated if those dependencies have been modified. The command used to execute the script is also embedded within the metadata of the figure. Note that only PDF figures are currently supported.

## Installing

The required dependencies should first be installed by running the following commands:

```
sudo pip3 install -U -r requirements.txt
sudo apt-get install texlive-latex-base
```

Pynea itself can then be installed with:

```
sudo python3 setup.py install
```

The `pynea.sty` file in the `tex` directory contains 3 custom macros for use in each figure environment. These macros assist Pynea in locating the relevant script and data files that are to be embedded. You can either copy this style file into the same directory as the .tex file you wish to compile, or copy it into your LaTeX installation to achieve a global installation.

## Usage

The `pynea` LaTeX style file should first be included in the LaTeX preamble using `\usepackage{pynea}`.

Each figure within the LaTeX document, specified using `\includegraphics`, can then be augmented with the following 3 statements:

* `\pyneascript{plot.py}` tells Pynea that the figure was generated using a file called `plot.py`.
* `\pyneacommand{python3 plot.py}` tells Pynea that the script is to be executed using `python3`.
* `\pyneadata{data1.dat data2.dat}` tells Pynea that the script depends on two data files, `data1.dat` and `data2.dat`.

For example, you may have something like:

```
\begin{figure}
  \includegraphics{/home/christian/my_paper/images/plot.pdf}
  \pyneascript{/home/christian/my_scripts/plot.py}
  \pyneacommand{python3 plot.py}
  \pyneadata{/home/christian/my_data/data1.txt /home/christian/my_data/data2.txt}
\end{figure}
```

Once all Pynea commands have been included in the figure environments, Pynea can be used to compile the document and embed the relevant files by running:

```
cd /path/to/document/directory
pynea example.tex
```

Opening the resulting document in a PDF viewer such as Adobe Reader and clicking the Attachments tab will list the embedded files.

## Contact

Please contact [Christian Jacobs](http://christianjacobs.uk) if you have any feedback about the project.
