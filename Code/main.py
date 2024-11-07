from utils import load_sequences
from sequence_aligner import SequenceAligner
from sequence_classifier import SequenceClassifier

def run_alignments(sequences):
    alignment_scores = []
    for i in range(len(sequences)):
        for j in range(i + 1, len(sequences)):
            seq1 = sequences[i].sequence
            seq2 = sequences[j].sequence

            aligner = SequenceAligner(seq1, seq2)
            global_alignment, global_score = aligner.perform_global_alignment()
            local_alignment, local_score = aligner.perform_local_alignment()

            alignment_scores.append((f"Global Alignment ({i+1} vs {j+1})", global_score))
            alignment_scores.append((f"Local Alignment ({i+1} vs {j+1})", local_score))

    return sorted(alignment_scores, key=lambda x: x[1])

def calculate_percentages(sequences):
    return [(f"Sequence {i+1}", seq.calculate_percentage()) for i, seq in enumerate(sequences)]

def classify_sequences(alignment_scores, threshold=900):
    classifier = SequenceClassifier(threshold)
    return [(pair, classifier.classify(score)) for pair, score in alignment_scores]
