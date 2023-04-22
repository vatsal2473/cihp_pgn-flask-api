from flask_cors import CORS
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_caching import Cache
import os
import shutil
import requests
import inf_pgn

def clean_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

cache = Cache()
app = Flask(__name__)
CORS(app)

app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)

def tmpfile_upload(path):
    files = {
        'file': open(path, 'rb'),
    }

    response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)

    url = response.json()['data']['url']
    url = url.replace('https://tmpfiles.org', 'https://tmpfiles.org/dl')

    return url

@app.route('/cihp_pgn_api', methods=['GET', 'POST'])
def cihp_pgn_api():
    if request.method == 'POST':
        file = request.files['file']
        clean_dir('upload')
        clean_dir('output')
        file.save(os.path.join('upload', file.filename))
        

    inf_pgn.main()

    output_filename = os.listdir('output/cihp_edge_maps/')[0]
    url1 = tmpfile_upload('output/cihp_edge_maps/' + output_filename)
    url2 = tmpfile_upload('output/cihp_parsing_maps/' + output_filename)
    
    # Return the results
    return jsonify({'cihp_edge_maps': url1, 'cihp_parsing_maps': url2})



if __name__ == "__main__":
    app.run(port=8000)