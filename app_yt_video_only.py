from flask import Flask, render_template, request, jsonify
from youtube import YTMetaData

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_youtube_link', methods=['POST'])
def check_youtube_link():
    data = check_link_and_get_meta()
    if data['success']:
        yt_meta = data['message']
        yt_title, yt_extra_info = yt_meta.refine(yt_meta.metadata['title'],refine_method="sub"), yt_meta.refine(yt_meta.metadata['author'])
        data['message'] = 'Title: ' + yt_title.lower() + '\n Desc: ' + yt_extra_info.lower()
    else:
        print(data['message'])
    return jsonify(data)


def check_link_and_get_meta():
    while True :
        try:
            # Receive the YouTube link from the frontend
            youtube_link = request.form.get('youtubeLink')

            # Perform your Python code here (e.g., check the link)
            # Replace the code below with your actual functionality
            # Example: Check if the link is not empty
            if not youtube_link:
                result = {'message': 'YouTube link is empty', 'success': False}
            else:
                yt_meta_info = YTMetaData(youtube_link)
                if yt_meta_info is not None:
                    result = {'message': yt_meta_info, 'success': True}
                else:
                    print('No videos ')
                    result = {'message': 'YouTube Video is no more !', 'success': False}
            return result

        except Exception as e:
            return {'message': 'Video not found!', 'success': False}

if __name__ == '__main__':
    app.run(debug=True)
