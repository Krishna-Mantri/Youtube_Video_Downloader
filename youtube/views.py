from django.shortcuts import render
import yt_dlp
import os

# Define download directory
DOWNLOAD_DIR = "downloads"

# Ensure the directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def progress_hook(d):
    """Handles download progress updates."""
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} - {d['_eta_str']} remaining")
    elif d['status'] == 'finished':
        print("Download complete!")

def youtube(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        format_choice = request.POST.get('format', 'video')  # Default to video
        
        # Define format options
        if format_choice == 'video':
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook]
            }
        elif format_choice == 'audio':
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [progress_hook]
            }
        else:
            return render(request, 'download.html', {"error": "Invalid format selected!"})

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            return render(request, 'download.html', {"message": "Download Complete!"})
        
        except yt_dlp.utils.DownloadError as e:
            return render(request, 'download.html', {"error": f"Download error: {str(e)}"})
        
        except Exception as e:
            return render(request, 'download.html', {"error": f"Unexpected error: {str(e)}"})

    return render(request, 'download.html')
