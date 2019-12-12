from app import app
from flask import render_template, url_for, request, jsonify
import base64
import requests
from . import timbre

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# just temporarily, only make sure I can get the analysis from Spotify
@app.route('/api/timbre_analysis', methods=['GET'] )
def timbre_analysis():
    # tenporarily hardcode the track id but the front end would normally send it in
    # the request
    # (this is Isis, from Bob Dylan Live 1975 Bootleg series)
    track_id = request.args.get('track_id') if request.args.get('track_id') else '2IfygshcMSLVv8b6DbgIoK'
    bySection = request.args.get('bySection') if request.args.get('bySection') else False

    # request audio analysis from Spotify
    # get access token
    client_string = CLIENT_ID + ":" + CLIENT_SECRET
    client_string = client_string.encode('utf-8')
    client_string = base64.urlsafe_b64encode(client_string)
    client_string = client_string.decode('utf-8')

    auth_string = f'Basic {client_string}'

    URL = 'https://accounts.spotify.com/api/token'
    response = requests.post(URL,
                        data = { 'grant_type' : 'client_credentials'},
                        headers = {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Authorization': auth_string
                        })

    response = response.json()
    token = response['access_token']
    expires_in = response['expires_in']

    # token = token.decode('utf-8')
    # get the audio analysis data for track_id
    URL = f'https://api.spotify.com/v1/audio-analysis/{track_id}'
    response = requests.get(URL,
                              headers= {
                                'Authorization' : f'Bearer {token}'
                              })

    # make the list of thetas
    audio_analysis_data = response.json()
    # get segment info  for now will only get timbre vectors + timing info
    segments = audio_analysis_data['segments']
    seg_info = timbre.getSegmentInfo(segments)
    # get section info.  for now only getting timing info for bySection precision
    sections = audio_analysis_data['sections']
    sect_info = timbre.getSectionInfo(sections)

    animation_data = timbre.getThetas(seg_info, sect_info, bySection=False, timescale_ms=None)

    # send the response to the front end
    return jsonify({
        'code': 200,
        'data': animation_data
    });
