from Bio import pairwise2
from Bio.pairwise2 import format_alignment

class SequenceAligner:
    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def perform_global_alignment(self):
        alignments = pairwise2.align.globalxx(self.seq1, self.seq2, one_alignment_only=True)
        best_alignment = alignments[0]
        return best_alignment, best_alignment[-1]

    def perform_local_alignment(self):
        alignments = pairwise2.align.localxx(self.seq1, self.seq2, one_alignment_only=True)
        best_alignment = alignments[0]
        return best_alignment, best_alignment[-1]

    def display_alignment(self, alignment):
        return format_alignment(*alignment)
