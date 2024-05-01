import mtranslate

class Translator:
    def __init__(self):
        pass
    
    def translate(self, text, lang):
        return mtranslate.translate(text, lang)