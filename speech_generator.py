class SpeechGenerator:
    def __init__(self, querier, translator, sentiment_analyzer, liwc_analyzer):
        self.querier = querier
        self.translator = translator
        self.sentiment_analyzer = sentiment_analyzer
        self.liwc_analyzer = liwc_analyzer
    
    def generate_base_speech(self, speech, requirements):
        prompt = """Read the instructions carefully to generate the output with tone, facial expressions, and emotions that aptly suit each statement.\n\n"""
        prompt += requirements
        prompt += "\n\n"
        prompt += "Generate the speech based on the given context and requirements. For each statement, add annotations for tone, facial expressions, and emotions in parentheses. For example: 'Ladies and gentlemen, my friends of Tamil Nadu, it's truly an honor to stand before you here in Chennai today, as we prepare for the crucial MP elections! (Warm smile, hands clasped together)'"
        prompt += "\n\nSpeech:\n"
        prompt += speech
        return self.querier.query(prompt)
    
    def get_metrics(self, speech):
        prompt = """You need to assess the following 5 personality traits from the below speech by giving it a score of 1 to 10 (discrete values) where 10 is the highest score and 1 is the lowest score (use floor value):
    (Agreeableness, Conscientiousness, Extraversion, Emotional range, Openness). Output should only be the scores with no extra text or information. Then regenerate the speech to improve the metrics and also sound more human.\n\n"""
        prompt += speech
        return self.querier.query(prompt)
    
    def enhance_eq_score(self, speech):
        sentiment = self.sentiment_analyzer.get_sentiment(speech)
        emotional_quotient = self.sentiment_analyzer.get_emotional_quotient(speech)
        prompt = """You are provided with speech and its Sentiment and Emotional Quotient. Add words to the speech such that the emotional quotient improves. Regenerate the speech accordingly.\n\n"""
        prompt += speech
        prompt += f"\nSentiment: {sentiment}\nEmotional Quotient: {emotional_quotient}"
        return self.querier.query(prompt)
    
    def enhance_liwc_metrics(self, speech):
        filtered_categories = self.liwc_analyzer.get_categories(speech)
        prompt = """You need to improvise the given speech text based on the provided information of Linguistic Inquiry and Word Count (LIWC).\n\n The Speech is: \n"""
        prompt += speech
        prompt += "\nLIWC information: \n\n"
        prompt += str(filtered_categories)
        return self.querier.query(prompt)
    
    def prime_speech(self, speech):
        prompt = """You need to assess the following speech for primings namely Issue Priming, Candidate Attributes Priming, Mood and Emotional Priming, Social Identity Priming, Economic Priming, Value-Based Priming, Repetition and Consistency, Visual and Symbolic Priming, Use of Surrogates and Endorsements, Framing and Issue Association, Contextual Priming. Give a rating for each metric on the scale of 10. 1 is the lowest and 10 is the highest.
Then, regenerate the speech by improving those metrics and make it sound more human. Output should only consist of the regenerated speech and nothing else. Do not even give any heading as Regenerated Speech, output should only be the regenerated speech itself.\n\n"""
        prompt += speech
        return self.querier.query(prompt)
    
    def filter_speech(self, speech):
        lines = speech.split("\n")
        filtered_lines = [line for line in lines if len(line.split()) > 1]
        filtered_text = "\n".join(filtered_lines)
        return filtered_text
    
    def translate_speech(self, speech, language):
        return self.translator.translate(speech, language)
    
    def generate_speech(self, speech, requirements, language="en"):
        
        base_speech = self.generate_base_speech(speech, requirements)
        
        
        personality_improved_speech = self.get_metrics(base_speech)
        

        eq_improved_speech = self.enhance_eq_score(personality_improved_speech)
        
        
        liwc_improved_speech = self.enhance_liwc_metrics(eq_improved_speech)
        
        
        primed_speech = self.prime_speech(liwc_improved_speech)
        
    
        filtered_speech = self.filter_speech(primed_speech)
        
    
        if language != "en":
            translated_speech = self.translate_speech(filtered_speech, language)
            return translated_speech
        
        return filtered_speech
