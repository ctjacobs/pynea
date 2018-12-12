# Pynea

Pynea facilitates the reproducibility of [LaTeX](https://www.latex-project.org/) documents by embedding the scripts and dependencies required to regenerate the figures within the document itself.

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

The `pynea.sty` file in the `tex` directory contains 3 custom macros for use in each figure environment. These macros assist Pynea in locating the relevant script and dependencies that are to be embedded. You can either copy this style file into the same directory as the .tex file you wish to compile, or copy it into your LaTeX installation to achieve a global installation.

## Usage

The `pynea` LaTeX style file should first be included in the LaTeX preamble using `\usepackage{pynea}`.

Each figure within the LaTeX document, specified using `\includegraphics`, can then be augmented with the following 3 statements:

* `\pyneascript{example.py}` tells Pynea that the figure was generated using a file called `example.py`.
* `\pyneacommand{python3 example.py}` tells Pynea that the script is to be executed using `python3`.
* `\pyneadependencies{example1.dat example2.dat}` tells Pynea that the script depends on two data files, `example1.dat` and `example2.dat`.

Once all Pynea commands have been included in the figure environments, Pynea can be used to compile the document and embed the relevant files by running:

```
cd /path/to/document/directory
pynea example.tex
```

Opening the resulting document in a PDF viewer such as Adobe Reader and clicking the Attachments tab will list the embedded files.

## Contact

Please contact [Christian Jacobs](http://christianjacobs.uk) if you have any feedback about the project.
