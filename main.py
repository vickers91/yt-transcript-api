from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

@app.route("/transcript", methods=["GET"])
def get_transcript():
    try:
        video_url = request.args.get("url")
        if not video_url:
            return jsonify({"error": "Missing URL"}), 400

        parsed_url = urlparse(video_url)
        video_id = parse_qs(parsed_url.query).get("v")

        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        video_id = video_id[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["pt", "en"])
        full_text = "\n".join([entry["text"] for entry in transcript])

        return jsonify({"transcript": full_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "API de Transcrição no ar! 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
