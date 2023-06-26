import threading
import webbrowser
from flask import Flask, render_template, request, jsonify
from heartquest_ML import MLModel
from flask_cors import CORS

# Change this line to specify the 'web' directory as your template_folder
app = Flask(__name__, static_url_path='', static_folder='web', template_folder='web')
CORS(app)  # This will allow JavaScript to make requests to your Flask server

model = None


@app.route('/')
def home():
    return app.send_static_file('index.html')
    

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    global model
    data = request.get_json()
    user_id = data.get('user_id')

    if user_id is None:
        print("User ID is not provided")
        return jsonify({'error': 'Missing "user_id" in request.'}), 400
    else:
        print("User ID is: ", user_id)

    if model is None:
        model = MLModel()

    recommendations = model.get_recommendations(user_id=user_id)

    if recommendations is None or len(recommendations) == 0:
        return jsonify({'error': 'No recommendations found.'}), 404

    return render_template('recommendations.html', recommendations=recommendations)


@app.route('/play_game', methods=['GET'])
def play():
    return render_template('game.html')

if __name__ == '__main__':
    # The Flask server runs on http://127.0.0.1:5000 by default, 
    # but it may be different depending on your setup.
    url = "http://127.0.0.1:5000/"
    webbrowser.open_new(url)
    app.run(debug=False)
