from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api

from TextSummarizer import TextSummarizer

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
text_summarizer = TextSummarizer()


class Index(Resource):
    def get(self):
        return {'description': 'API to summarize texts', 
                'routes': ['GET / - general info', 
                           'POST /text-to-summarize - return summarized text, number of words and sentences and time of reading']}


class TextSummarize(Resource):
    @cross_origin()
    def post(self):
        data = request.get_json()
        text = data.get('text', '') 
        percent = data.get('percent', '')
        return text_summarizer.generate_summary(text, percent)
    

api.add_resource(Index, '/')    
api.add_resource(TextSummarize, '/text-to-summarize')

if __name__ == '__main__':
    app.run(debug=True)