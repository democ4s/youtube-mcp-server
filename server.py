from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

mcp = FastMCP(
    "YouTubeTools", 
    dependencies=["yt-dlp", "youtube-transcript-api"],
    host="0.0.0.0",
    port=8000
)

@mcp.tool(title="Get YouTube Video ID")
def get_video_id(url: str) -> str:
    """Extract the video ID from a YouTube URL"""
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['id']

@mcp.tool(title="Get YouTube Transcript")
def get_transcript(video_id: str) -> str:
    """Get the full transcript of a YouTube video"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(entry['text'] for entry in transcript)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")