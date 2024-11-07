from Bio import SeqIO

class DNASequence:
    def __init__(self, filename):
        self.filename = filename
        self.sequence = self._load_sequence()

    def _load_sequence(self):
        return SeqIO.read(self.filename, 'fasta').seq

    def calculate_percentage(self):
        total_bases = len(self.sequence)
        percentages = {
            'C': (self.sequence.count('C') / total_bases) * 100,
            'G': (self.sequence.count('G') / total_bases) * 100,
            'T': (self.sequence.count('T') / total_bases) * 100,
            'A': (self.sequence.count('A') / total_bases) * 100,
            'CG': (self.sequence.count('CG') / total_bases) * 100
        }
        return percentages
