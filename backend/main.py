from flask import Flask, request, jsonify
import keras._tf_keras.keras as tfk
from pgen import RapGenerator
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
print(cors)


# Flask endpoint to generate rap lyrics
@app.route("/generate", methods=["POST"])
def generate_rap():
    try:
        data = request.get_json()
        selected_artists = data.get("artists", [])
        selected_artists = sorted(selected_artists)

        unique_name = f"combined_{'_'.join(selected_artists)}"

        filenames = []
        for artist in selected_artists:
            filenames.append(f"./song_lyrics/{artist}.txt")

        # Use UTF-8 encoding when reading and writing files
        with open(f"./song_lyrics/{unique_name}.txt", "w", encoding="utf-8") as outfile:
            for fname in filenames:
                try:
                    with open(fname, encoding="utf-8") as infile:
                        for line in infile:
                            outfile.write(line)
                except FileNotFoundError:
                    print(f"File not found: {fname}")
                except UnicodeDecodeError as e:
                    print(f"Error decoding {fname}: {e}")
        deep_learning_model = unique_name
        depth = 4
        max_syllables = 8
        training_file = f"./song_lyrics/{unique_name}.txt"
        rap_gen = RapGenerator(deep_learning_model, training_file, max_syllables, depth)
        model_path = f"./{unique_name}.rap.weights.h5"

        if os.path.exists(model_path):
            result = rap_gen.main(train_mode=False)
        else:
            rap_gen.main(train_mode=True)
            result = rap_gen.main(train_mode=False)
        return (
            jsonify({"status": "success", "lyrics": result}),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Flask endpoint to train the model
@app.route("/train", methods=["GET"])
def train_model():
    try:
        # # Train the model
        # deep_learning_model = "poem_model"
        # depth = 4
        # max_syllables = 8
        # training_file = tfk.utils.get_file(
        #     "hello.txt",
        #     "https://storage.googleapis.com/kagglesdsdata/datasets/6776/19383/notorious_big.txt",
        # )
        # rap_gen = RapGenerator(deep_learning_model, training_file, max_syllables, depth)
        # result = rap_gen.main(train_mode=True)
        # # rap_generator.main(train_mode=True)
        print("hitted the train api")
        return (
            jsonify({"status": 200, "message": "model trained hitted"}),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Flask endpoint for health check
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "success", "message": "API is running!"}), 200


# Run the Flask app
if __name__ == "__main__":
    # Make sure the server runs on the desired port
    app.run(host="127.0.0.1", port=5000, debug=True)
