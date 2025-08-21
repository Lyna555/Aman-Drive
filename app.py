from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from dbconfig import db, DATABASE_URI
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import librosa
import os

from models import *
from middlewares import token_required, role_required

from routes.user_routes import user_bp
from routes.client_routes import client_bp
from routes.insurance_routes import insurance_bp
from routes.accident_routes import accident_bp
from routes.police_routes import police_bp

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.register_blueprint(user_bp)
app.register_blueprint(client_bp)
app.register_blueprint(insurance_bp)
app.register_blueprint(accident_bp)
app.register_blueprint(police_bp)

jwt = JWTManager(app)

db.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

#with app.app_context():
#    db.create_all()
#    print("✅ Tables created successfully!")

with app.app_context():
    from controllers.accident_controller import find_closest_police
    print(find_closest_police("https://maps.app.goo.gl/CMnMw3XuVPPt15Ys7"))

interpreter = tf.lite.Interpreter(model_path='car_crash_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

SR = 22050
N_MELS = 128
MAX_LEN = 216
DURATION = 5.0
N_FFT = 1024
HOP_LENGTH = 256

def extract_features(file_path, sr=SR, n_mels=N_MELS, max_len=MAX_LEN):
    audio, _ = librosa.load(file_path, sr=sr, duration=DURATION, mono=True)
    mel_spec = librosa.feature.melspectrogram(
        y=audio, sr=sr, n_mels=n_mels, n_fft=N_FFT, hop_length=HOP_LENGTH
    )
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    if mel_spec_db.shape[1] < max_len:
        pad_width = max_len - mel_spec_db.shape[1]
        mel_spec_db = np.pad(
            mel_spec_db,
            pad_width=((0, 0), (0, pad_width)),
            mode='constant',
            constant_values=(np.min(mel_spec_db),)
        )
    else:
        mel_spec_db = mel_spec_db[:, :max_len]

    return mel_spec_db.astype(np.float32)

@app.route('/')
def index():
    return 'Welcome to Aman Drive!'

@app.route('/predict', methods=['POST'])
@token_required
@role_required('client')
def predict(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            file_path = tmp.name
            file.save(file_path)

        # Extract features
        features = extract_features(file_path)
        features = np.expand_dims(features, axis=-1)  # (128, 216, 1)
        features = np.expand_dims(features, axis=0)   # (1, 128, 216, 1)

        # Predict
        interpreter.set_tensor(input_details[0]['index'], features)
        interpreter.invoke()
        
        output_data = interpreter.get_tensor(output_details[0]['index'])
        prediction_prob = float(output_data[0][0])  # for sigmoid
        predicted_class = int(prediction_prob > 0.5)

        print("Prediction prob:", prediction_prob)
        print("Predicted class:", predicted_class)

        # Remove temp file
        os.remove(file_path)

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': prediction_prob
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
