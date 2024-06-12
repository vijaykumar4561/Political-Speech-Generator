class SpeechGenerator:
    def __init__(self, querier, translator, sentiment_analyzer, liwc_analyzer):
        self.querier = querier
        self.translator = translator
        self.sentiment_analyzer = sentiment_analyzer
        self.liwc_analyzer = liwc_analyzer

    def generate_message(self, topic, emotion):
        prompt = f"Generate a campaign message about {topic} that evokes a sense of {emotion}."
        generated_text = generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']
        return generated_text

    def create_positive_association(self, candidate_name, theme):
        prompt = f"Write a sentence that associates {candidate_name} with {theme}."
        generated_text = generator(prompt, max_length=30, num_return_sequences=1)[0]['generated_text']
        return generated_text

    def craft_story(self, candidate_name, values, aspirations):
        prompt = (f"Create a compelling story for the campaign of {candidate_name} that touches on values like {values} "
                  f"and aspirations such as {aspirations}.")
        story = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
        return story

    def automated_response(self, user_message):
        sentiment = self.sentiment_analyzer.get_sentiment(user_message)
        if sentiment['compound'] < -0.3:
            response = random.choice([
                "I'm sorry to hear that you're feeling this way. We understand your concerns and are working hard to address them.",
                "We appreciate your feedback and are here to listen. Let's work together to find a solution."
            ])
        elif sentiment['compound'] > 0.3:
            response = random.choice([
                "Thank you for your support! We're committed to making a positive impact.",
                "We're glad to hear your positive feedback. Together, we can achieve great things!"
            ])
        else:
            response = random.choice([
                "Thank you for reaching out. Your thoughts are important to us.",
                "We value your input and are dedicated to addressing the issues that matter to you."
            ])
        return response

    def generate_base_speech(self, speech, requirements):
        prompt = """Read the instructions carefully to generate the output\n\n"""
        prompt += requirements
        prompt += "\n"
        prompt += speech
        return self.querier.query(prompt)

    def get_metrics(self, old_speech):
        prompt = """You need to assess the following 5 personality traits from the below speech by giving it a score of 1 to 10 (discrete values) where 10 is the highest score and 1 is the lowest score (use floor value):
    (Agreeableness, Conscientiousness, Extraversion, Emotional range, Openness). Output should only be the scores with no extra text or information. Then regenerate the speech to improve the metrics and also sound more human\n\n"""
        prompt += old_speech
        return self.querier.query(prompt)

    def enhance_eq_score(self, generated_speech):
        sentiment = self.sentiment_analyzer.get_sentiment(generated_speech)
        emotional_quotient = self.sentiment_analyzer.get_emotional_quotient(generated_speech)
        prompt = """You are provided with speech and its Sentiment and Emotional Quotient. Add words to speech such that emotional quotient improves. Regenerate the speech accordingly.\n\n"""
        prompt += generated_speech
        prompt += f"\nSentiment:{sentiment}\nEmotional Quotient:{emotional_quotient}"
        return self.querier.query(prompt)

    def enhance_liwc_metrics(self, generated_speech):
        filtered_categories = self.liwc_analyzer.get_categories(generated_speech)
        prompt = """You need to improvise the given speech text based on the provided information of Linguistic Inquiry and Word Count LIWC.\n\n The Speech is: \n"""
        prompt += generated_speech
        prompt += "LIWC information: \n\n"
        prompt += str(filtered_categories)
        return self.querier.query(prompt)

    def prime_speech(self, generated_speech):
        prompt = """You need to assess the following speech for primings namely Issue Priming, Candidate Attributes Priming, Mood and Emotional Priming, Social Identity Priming, Economic Priming, Value-Based Priming, Repetition and Consistency, Visual and Symbolic Priming Use of Surrogates and Endorsements, Framing and Issue Association,Contextual Priming. Give a rating for each metric on the scale of 10. 1 is the lowest and 10 is the highest. 
Then, regenerate the speech by improving those metrics and make it sound more human. Output should only consist of the regenerated speech and nothing else. Do not even give any heading as Regenerated Speech, output should only be the regenerated speech itself.\n\n"""
        prompt += generated_speech
        return self.querier.query(prompt)

    def filter_speech(self, generated_speech):
        text = generated_speech
        lines = text.split("\n")
        filtered_lines = [line for line in lines if len(line.split()) > 1]
        filtered_text = "\n".join(filtered_lines)
        return filtered_text

    def translate_speech(self, generated_speech, language):
        return self.translator.translate(generated_speech, language)

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


