from flasgger import swag_from
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask import request
import pandas as pd
from flask import Flask, jsonify
from function import full_clean
import sqlite3

# connect to sqlite
con = sqlite3.connect('api.db')
cur = con.cursor()

df_1 = pd.read_sql("SELECT Tweet from data", con)

con.close()


# Flask and Swagger UI
app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info={
        'title': LazyString(lambda: 'Text Cleansing API Documentation'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'API untuk membersihkan text data')
    },
    host=LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

# First endpoint to process text input


@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': full_clean(text)  # full clean function from function.py
    }

    response_data = jsonify(json_response)
    return response_data

# second endpoint to process file input


@swag_from("docs/text_processing_file.yml", methods=['GET'])
@app.route('/text-processing-file', methods=['GET'])
def GET():

    df_list = []
    for i, k in df_1.iterrows():
        # apply function to every row in df_1 column tweet
        df_list.append(full_clean(k['Tweet']))

    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': df_list
    }

    response_data = jsonify(json_response)
    return response_data


if __name__ == '__main__':
    app.run(debug=True)
