# Percent_aligned
Calculate percent of reference nucleotides in aligned regions from bam file

## Input
* A reference genome (single or multifasta)
* An alignment file in BAM format

## Dependencies
* bedtools
* Python v3.5 or greater. Following packages required:
  * argparse
  * os
  * tempfile
  * subprocess
  * sys
  * Bio
  
## Running Program
`python percent_aligned.py -g [reference_genome] -b [bam_file]`

## Results
Will output a `perc_aligned.results.txt` with the following format (tab deliminated):

`reference_genome bam_file sequence_in_reference percent_aligned`

**sequence_in_reference** --> In fasta file, each sequence will get its own line

**percent_aligned** --> What percent of the nucleotides in **sequence_in_reference** contains at least 1 aligned read
