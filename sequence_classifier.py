class SequenceClassifier:
    def __init__(self, threshold):
        self.threshold = threshold

    def classify(self, alignment_score):
        return "Similar" if alignment_score >= self.threshold else "Not Similar"
