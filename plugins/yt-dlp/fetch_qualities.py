import sys
import json
import yt_dlp

def is_youtube_url(url):
    return 'youtube.com' in url or 'youtu.be' in url

def fetch_qualities(url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best'
    }

    # Use cookies.txt only for YouTube URLs
    if is_youtube_url(url):
        ydl_opts['cookiefile'] = 'cookies.txt'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            
            # Extract all format options with their quality, format type, and size
            format_list = []
            for fmt in formats:
                format_id = fmt.get('format_id', 'unknown')
                format_label = fmt.get('format', 'Unknown Format')
                file_size = fmt.get('filesize') or fmt.get('filesize_approx')  # File size in bytes

                size_str = f"{file_size / (1024 * 1024):.2f} MB" if file_size else "Unknown size"

                if 'height' in fmt:
                    label = f"{fmt['height']}p ({format_label}, {size_str})"
                else:
                    label = f"Audio ({format_label}, {size_str})"
                
                format_list.append({'id': format_id, 'label': label})

            return json.dumps(format_list)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return json.dumps({'error': error_message})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(fetch_qualities(url))
    else:
        print(json.dumps({'error': 'No URL provided'}))
        sys.exit(1)
