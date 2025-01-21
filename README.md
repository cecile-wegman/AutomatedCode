# Mutation Data Processing and Visualization Tools

This repository provides tools for processing genetic mutation data, generating statistics, and visualizing mutation frequencies. It includes scripts written in Python, R, and PowerShell to streamline workflows for genetic analysis.

## Installation

### Python Dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required Python libraries:
`pip install pandas argparse`

### R Dependencies
Install the necessary R packages in your R environment:
`install.packages(c("ggplot2", "dplyr", "stringr", "readxl", "tidyverse"))`

## Usage

1. Generate `regions.txt` using `Generate_positions.py`:
`python Generate_positions.py <input_tsv_file>`

2. Parse BAM readcount data using `Parce_brc.py`:
`python Parce_brc.py <input_bam_readcount_file> --encoding <optional_encoding>`

3. Automate genome processing using `Process_genome.ps1` (requires Docker):
`./Process_genome.ps1`

4. Visualize mutation data using `Plot_visualization.R` in RStudio. Modify file paths as necessary and execute the script.

## Features

- Automates the generation, sorting, and parsing of genome data.
- Processes BAM readcount output into detailed TSV reports.
- Visualizes mutation frequencies with customizable plots.

## Example Workflow

1. Generate regions:
`python Generate_positions.py example.tsv`

2. Parse BAM readcount data:
`python Parce_brc.py example.bam.tsv`

3. Run genome processing pipeline:
`./Process_genome.ps1`

4. Visualize mutation frequencies:
Run `Plot_visualization.R` in RStudio.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes. Please make sure to update tests as appropriate.
