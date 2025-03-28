from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json

def handler(request):
    try:
        if request.method == "GET":
            video_url = request.args.get("url")
        elif request.method == "POST":
            body = request.get_json()
            video_url = body.get("url")
        else:
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Method not allowed"})
            }

        # Extrair o ID do vídeo
        parsed_url = urlparse(video_url)
        video_id = parse_qs(parsed_url.query).get("v")

        if not video_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid YouTube URL"})
            }

        video_id = video_id[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        full_text = "\n".join([entry['text'] for entry in transcript])

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"transcript": full_text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

