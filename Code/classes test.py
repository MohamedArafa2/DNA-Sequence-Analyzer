from Bio import SeqIO, AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Align.Applications import ClustalwCommandline
from ete3 import Tree as ETE3Tree
import numpy as np
import matplotlib.pyplot as plt

class DNAAnalysisTool:
    def __init__(self):
        pass

    def load_sequences(self, file_paths):
        """Load DNA sequences from FASTA files."""
        sequences = []
        for file_path in file_paths:
            with open(file_path, "r") as file:
                for record in SeqIO.parse(file, "fasta"):
                    sequences.append(record)
        return sequences

    def multiple_sequence_alignment(self, sequences):
        """Perform multiple sequence alignment using Clustal Omega."""
        alignment_file = "aligned_sequences.aln"
        SeqIO.write(sequences, "temp.fasta", "fasta")
        clustalw_exe = "clustalw2"  # Make sure ClustalW is installed and in PATH
        clustalw_cline = ClustalwCommandline(clustalw_exe, infile="temp.fasta")
        stdout, stderr = clustalw_cline()
        alignment = AlignIO.read(alignment_file, "clustal")
        return alignment

    def construct_phylogenetic_tree(self, alignment):
        """Construct a phylogenetic tree from the alignment."""
        from Bio.Phylo import distance
        # Calculate a distance matrix
        dm = distance.pdist(alignment)
        # Create a tree from the distance matrix (you may need to choose the right method)
        # Here you would typically use a specific method to create a tree, e.g., UPGMA or Neighbor-Joining
        # For simplicity, let's assume you have a Newick string or a method to create it
        newick_str = "((A,B),C);"  # Placeholder for actual Newick string
        tree = ETE3Tree(newick_str)
        return tree

    def detect_mutations(self, alignment):
        """Detect mutations and SNPs in the aligned sequences."""
        mutations = []
        for i in range(alignment.get_alignment_length()):
            column = alignment[:, i]
            if len(set(column)) > 1:  # More than one unique base
                mutations.append((i, column))
        return mutations

    def identify_conserved_regions(self, alignment):
        """Identify conserved regions across sequences."""
        consensus = alignment.consensus()
        conserved_regions = [i for i, base in enumerate(consensus) if base != '-']
        return conserved_regions

    def generate_report(self, mutations, conserved_regions):
        """Generate a report of findings."""
        report = "Mutations:\n"
        for mutation in mutations:
            report += f"Position {mutation[0]}: {mutation[1]}\n"
        report += "\nConserved Regions:\n"
        report += ", ".join(map(str, conserved_regions))
        return report

if __name__ == "__main__":
    # Define paths to your FASTA files
    br_sequences = [f'data/br_{i}.fasta' for i in range(1, 2)]
    lung_sequences = [f'data/lung{i}.fasta' for i in range(1, 2)]

    # Initialize the tool
    tool = DNAAnalysisTool()

    # Load sequences
    br_seqs = tool.load_sequences(br_sequences)
    lung_seqs = tool.load_sequences(lung_sequences)
    lung_seqs1 = tool.load_sequences(lung_sequences)


    # Perform multiple sequence alignment
    alignment = tool.multiple_sequence_alignment(br_seqs)

    # Construct phylogenetic tree
    tree = tool.construct_phylogenetic_tree(alignment)

    # Detect mutations
    mutations = tool.detect_mutations(alignment)

    # Identify conserved regions
    conserved_regions = tool.identify_conserved_regions(alignment)

    # Generate report
    report = tool