from flask import Flask, render_template, request, jsonify, render_template_string
from yt_scrape import ScrapeYT_Channel
import random 
from yt_utils import extract_important_words_entities, extract_important_words_subjects
from diffusion_model import StableDiffusion
from torch import autocast
import time
from numpy import asarray
import cv2 
import base64
import json

app = Flask(__name__)
# python -m spacy download en_core_web_sm

YTScrape = ScrapeYT_Channel()

@app.route('/')
def index():
    return render_template('index.html')

# stablePipeline = StableDiffusion(modelid="runwayml/stable-diffusion-v1-5")
stablePipeline = StableDiffusion()
print('CALLED MAIN FILE')

@app.route('/get_new_hint', methods=['POST'])
def get_new_hint():

    hint_type = request.json.get('hint_type')
    # Parse the JSON string into a Python list
    all_hints_json = request.json.get('all_hints')
    all_hints = json.loads(all_hints_json)
    hint_idx = request.json.get('curr_idx')

    if hint_idx >= len(all_hints):
        return jsonify({'success': False})

    hint = all_hints[hint_idx]
    if hint_type == "text":
        return jsonify({'hint': hint, 'success': True })

    img = stablePipeline.generate_img(hint)
    img = asarray(img)
    # img = cv2.imread('output.png')
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convert the image to base64 encoding
    _, encoded_image = cv2.imencode('.png', img)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')
    hint = render_template_string('<img src="data:image/png;base64,{{ image }}" alt="Generated Image">', image=base64_image)
    return jsonify({'hint': hint, 'success': True})

@app.route('/check_youtube_link', methods=['POST'])
def check_youtube_link():
    data = check_link_and_get_meta()
    hint_type = request.form.get('hint_type')
    if hint_type == "image":
        all_hint_images = []

    data['image_links'] = None
    if data['success'] and len(data['message']) >= 4:
        print(len(data['message']))
        target = random.sample(data['message'], 1)
        options = random.sample(data['message'], 3)
        if data['type'] == "shorts":
            target_text = target[0]['headline']['simpleText']
        else:
            target_text = target[0]['title']['runs'][0]['text']

        all_hints = extract_important_words_subjects(target_text, data['type'], curr_search=data['curr_search'])
        if hint_type == "image":
            all_hints.sort(key=lambda x: -len(x))

        target_img_url = target[0]['thumbnail']['thumbnails'][-1]['url']
        target_vid_url = target[0]['videoId']
        target_id = target[0]['targetId']
        options_imgs = [(target_img_url, target_vid_url, target_id, target_text)] 
        for i in range(len(options)):
            curr_img_url = options[i]['thumbnail']['thumbnails'][-1]['url']
            curr_yt_vid_url = options[i]['videoId']
            curr_id = options[i]['targetId']
            if data['type'] == "shorts":
                curr_text = options[i]['headline']['simpleText']
            else:
                curr_text = options[i]['title']['runs'][0]['text']
            options_imgs.append((curr_img_url, curr_yt_vid_url, curr_id, curr_text))

        random.shuffle(options_imgs)
        ## need to to do lemmaization 
        data['message'] = target_text.lower()
        data['image_links'] = options_imgs
        data['target'] = target_id
        data['hints'] = all_hints
        print(all_hints)
        # data['lemma_target_text'] = lemma_target_text
    else:
        data['message'] = "Not enough content ! / Enter the actual channel address: youtube.com/@<channel_name>"
        data['hints'] = []
        data['success'] = False
        print(data['message'], data['success'])
    return data
    return jsonify(data)


def check_link_and_get_meta():
    while True :
        try:
            # Receive the YouTube link from the frontend
            search_type = request.form.get('selectedOption')
            youtube_link = request.form.get('youtubeLink')

            # Perform your Python code here (e.g., check the link)
            # Replace the code below with your actual functionality
            # Example: Check if the link is not empty
            if not youtube_link:
                result = {'message': 'YouTube link is empty', 'success': False}
            else:
                YTScrape.get_yt_url(youtube_link)
                YTScrape.content_type = search_type
                yt_catalog_info, isSuccess = YTScrape.get_channel_vids_info()
                result = {'message': yt_catalog_info, 'success': isSuccess, 'type': search_type, 'curr_search': youtube_link}
            return result

        except Exception as e:
            return {'message': 'Video not found!', 'success': False}

if __name__ == '__main__':
    print('CALLED APP FILE')
    app.run(debug=False)
