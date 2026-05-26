from flask import Flask, render_template, request
import os

from deep_translator import GoogleTranslator
from gtts import gTTS

from model.caption_generator import generate_caption

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
AUDIO_FOLDER = "static/audio"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():

    caption = None
    translated_caption = None
    image_path = None
    audio_path = None

    if request.method == "POST":

        image = request.files["image"]
        language = request.form["language"]

        if image:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                image.filename
            )

            image.save(filepath)

            # Generate caption
            caption = generate_caption(filepath)

            # Translate caption
            translated_caption = GoogleTranslator(
                source='auto',
                target=language
            ).translate(caption)

            # Generate audio
            tts = gTTS(
                translated_caption,
                lang=language
            )

            audio_file = "caption.mp3"

            audio_path = os.path.join(
                app.config["AUDIO_FOLDER"],
                audio_file
            )

            tts.save(audio_path)

            image_path = filepath

    return render_template(
        "index.html",
        caption=caption,
        translated_caption=translated_caption,
        image_path=image_path,
        audio_path=audio_path
    )


if __name__ == "__main__":
    app.run(debug=True)