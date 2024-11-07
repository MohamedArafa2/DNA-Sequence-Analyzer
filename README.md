# DNA Sequence Analyzer

A bioinformatics tool for analyzing DNA sequences, performing global and local alignments, calculating nucleotide percentages, and classifying sequences based on alignment scores. The tool also includes a graphical user interface (GUI) using Tkinter, and users can save the results in an Excel file.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)


## Installation

### 1. Clone the Repository

```bas# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```
### 2. Install Dependencies
```
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt
```
The main dependencies are:
1.biopython.
2.pandas.
3.matplotlib.
4.tkinter.

### 3. Running the Application
```
python main_gui.py

```
# Usage
1. Load DNA Sequences
Click on the "Browse Files" button to upload FASTA files containing DNA sequences.
2. Perform Alignments
Click on "Perform Alignment" to compute both global and local alignments for the sequences.
3. Calculate Nucleotide Percentages
Click on "Calculate Percentages" to compute the percentages of each nucleotide (A, T, G, C) and the CG dinucleotide.
4. Classify Sequences
Set a threshold value for classification (default: 900) and click "Classify Sequences" to classify sequences as similar or not similar based on the alignment scores.
5. Save Output
Optionally, save the results (alignment scores, percentages, and classifications) to an Excel file by clicking the "Save Output" button.

## Example Workflow
Upload Files: Select one or more DNA sequence files in FASTA format.
Align Sequences: Perform global and local alignments between all sequences.
Calculate Percentages: Calculate the percentages of A, T, G, C, and CG nucleotides.
Classify Sequences: Classify sequences as "Similar" or "Not Similar" based on the alignment scores.
Save Results: Save all results to an Excel file.

## Features

- **DNA Sequence Analysis**: Load DNA sequences from FASTA files and calculate nucleotide percentages (A, T, G, C, and CG).
- **Sequence Alignment**: Perform global and local alignment of DNA sequences using Biopython's `pairwise2`.
- **Classification**: Classify sequences based on their alignment score using a customizable threshold.
- **Graphical User Interface**: Intuitive GUI built using Tkinter for easy interaction with the tool.
- **Save Results**: Save alignment scores, nucleotide percentages, and classifications to an Excel file.


