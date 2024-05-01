from flask import Flask, request, jsonify
from flask_cors import CORS
from speech_generator import SpeechGenerator
from translator import Translator
from querier import Querier
from sentiment_analyzer import SentimentAnalyzer
from liwc_analyzer import LIWCAnalyzer

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, World!', 200

@app.route('/generate_speech', methods=['POST'])
def generate_speech():
    data = request.get_json()
    speech, requirements = data['speech'], data['requirements']
    print('Generating speech...')
    generated_speech = speech_generator.generate_speech(speech, requirements)
    response = {
        'generated_speech': generated_speech
    }
    return jsonify(response), 200

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    speech, language = data['speech'], data['language']
    lang_abbr = {
        'Hindi': 'hi',
        'Telugu': 'te',
        'Bengali': 'bn'
    }
    lang = lang_abbr[language]
    translated_speech = translator.translate(speech, lang)
    response = {
        'translated_speech': translated_speech
    }
    return jsonify(response), 200

if __name__ == '__main__':

    querier = Querier()

    translator = Translator()

    sentiment_analyzer = SentimentAnalyzer()

    liwc_analyzer = LIWCAnalyzer()

    speech_generator = SpeechGenerator(querier, translator, sentiment_analyzer, liwc_analyzer)

    app.run(host='0.0.0.0', port=10000)
