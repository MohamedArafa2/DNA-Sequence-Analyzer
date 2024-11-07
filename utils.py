from dna_sequence import DNASequence

def load_sequences(filenames):
    return [DNASequence(filename) for filename in filenames]
