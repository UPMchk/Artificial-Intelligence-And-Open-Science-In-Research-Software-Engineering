# Artificial-Intelligence-And-Open-Science-In-Research-Software-Engineering

# Assignment 1 - Grobid analysis of open-access papers

## Overview
This project analyzes 10 open-access research articles using Grobid.

The project generates:
- a keyword cloud based on the abstracts
- a visualization of the number of figures per article
- a list of links found in each paper

## Dataset
The dataset consists of 10 open-access PDF papers related to open science, reproducibility and research software engineering.

## Repository structure
- `data/pdfs/`: input PDF files
- `data/tei/`: TEI/XML files extracted with Grobid
- `src/`: source code
- `results/`: generated outputs
- `tests/`: tests

## Outputs
The project generates the following files:
- `results/abstracts.csv`
- `results/figures_per_paper.csv`
- `results/figures_per_paper.png`
- `results/links_per_paper.csv`
- `results/keyword_cloud.png`

## Current status
The PDF to TEI/XML extraction pipeline has been completed using Grobid.
The XML files were parsed to extract abstracts, figure counts and links.
A figure-count visualization and a keyword cloud have already been generated.

## How to run
1. Place the input PDF files in `data/pdfs/`
2. Extract TEI/XML files with Grobid into `data/tei/`
3. Run:
   - `py src/parse_tei.py`
   - `py src/make_figures_plot.py`
   - `py src/make_wordcloud.py`

## Notes
Some papers may have incomplete metadata extraction depending on the PDF structure and Grobid parsing quality.
