from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json

def handler(event, context):
    try:
        query = event.get("queryStringParameters", {})
        video_url = query.get("url", "")

        parsed_url = urlparse(video_url)
        video_id = parse_qs(parsed_url.query).get("v")

        if not video_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid YouTube URL"})
            }

        video_id = video_id[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["pt", "en"])
        full_text = "\n".join([entry["text"] for entry in transcript])

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
