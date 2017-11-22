import argparse
import os
import tempfile
from subprocess import PIPE, call, run
import sys
from Bio import SeqIO

#########################
######## PARSER #########
#########################
parser = argparse.ArgumentParser(description="Get percent of reference nucleotides contain >0 aligned reads")

#parser arguments
parser.add_argument("-b", "--bam", help = "BAM file", type = str)
parser.add_argument("-g", "--genome", help = "Reference genome [Fasta]", type = str)

#initiat parser
#print help if no arguments given
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
args = parser.parse_args()

##############################
######### FUNCTIONS ##########
##############################

'''
capture output from terminal command as string
'''
def out(command):
    result = run(
            command,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
            shell=True)
    return result.stdout.rstrip()


'''
return a dictionary with sequence name (key) and sequence lengh (value)
example output:
{'gnl|NISC|tig00000000_chr': 4508286,
 'gnl|NISC|tig00000001': 310952}
'''
def seq_name_length(fasta):
    fasta_list = {}
    for rec in SeqIO.parse(fasta, "fasta"):
        name = rec.id
        seqLen = len(rec)
        fasta = {name:seqLen}
        fasta_list[name] = seqLen
    return fasta_list #returns a dictionary with fasta ID as key, length as value



'''
Run genomecov to extract the nucleotide positions that have no aligned reads.
Will create a temp1 file containing data.
Example output:

gnl|NISC|tig00000000_chr	135006	0
gnl|NISC|tig00000000_chr	135007	0
gnl|NISC|tig00000000_chr	135008	0
gnl|NISC|tig00000000_chr	135009	0

to do: get this so it's in dictionary format as well...
{'gnl|NISC|tig00000000_chr': 4060,
 'gnl|NISC|tig00000001': 590}
'''
def get_zeros(bamfile, genomefile):
    zeros_file = tempfile.NamedTemporaryFile(dir=".", mode = "r")
    genome_cov_command = "bedtools genomecov -d -ibam %s -g %s | awk '$3==0'" % (bamfile, genomefile)
    call(genome_cov_command, shell = True, stdout = zeros_file)
    genome_names = []
    genome_counts = []
    for rec in SeqIO.parse(genomefile, "fasta"):
        name = rec.id
        genome_names.append(name)
    for name in genome_names:
        count = out("cat '%s' | grep '%s' | wc -l" % (zeros_file.name, name))
        genome_counts.append(int(count))
    zeros_file.close()
    return dict(zip(genome_names, genome_counts))



'''
Takes two dictionaries as arguments. One shows sequence name and length:
foo_len = {'chr1':102, 'chr2':203}

The other shoes sequence name and number of unaligned nucleotides:
foo_zeros = {'chr1':17, 'chr2':100}

Computes percent of sequences aligned
'''
def perc_nonzero(dic1, dic2):
    final = {}
    dic_keys = list(dic1.keys())
    for k in dic_keys:
        k_len = dic1[k]
        k_zeros = dic2[k]
        if k_len < k_zeros:
            print("More zeros than length of genome")
            sys.exit()
        zeros = k_zeros / k_len
        perc_aligned = format((1 - zeros) * 100.00, '.3f')
        d = {k:float(perc_aligned)}
        final.update(d)
        return_statement = "%s\t%s\t%s\t%s\n" % (args.genome, args.bam, k, str(perc_aligned))
        with open("perc_aligned.results.txt", "a") as results:
            results.write(return_statement)


#####################
#### RUN PROGRAM ####
#####################
def main():
    dic1 = seq_name_length(args.genome)
    dic2 = get_zeros(args.bam, args.genome)
    perc_nonzero(dic1, dic2)

if __name__ == '__main__':
    main()
