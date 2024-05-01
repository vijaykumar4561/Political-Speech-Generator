from empath import Empath

class LIWCAnalyzer:
    def __init__(self):
        self.lexicon = Empath()
    
    def get_categories(self, text):
        categories = self.lexicon.analyze(text)
        filtered_categories = {key: value for key, value in categories.items() if value != 0}
        return filtered_categories