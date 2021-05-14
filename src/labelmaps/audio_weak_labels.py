
class AudioWeakLabels:
    def __init__(self):
        self.multilabel = True
        self.multiclass = True

        self.label_dict = {
            "classes": [],
            "labels": []
        }