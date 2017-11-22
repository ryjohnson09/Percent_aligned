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
`python percent_aligned.py -g [reference_genome] -b [BAM file]`
