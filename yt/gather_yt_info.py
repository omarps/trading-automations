import sys
import yt_dlp as youtube_dl
from datetime import timedelta
import subprocess

def seconds_to_time_format(seconds, time_format="%H:%M:%S"):
    # Create a timedelta object
    delta = timedelta(seconds=seconds)
    # Extract hours, minutes, and seconds from the timedelta
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Format the time as HH:MM:SS
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Example usage
# milliseconds = 123456789
# formatted_time = milliseconds_to_time_format(milliseconds)
# print(formatted_time)  # Output: 34:17:36

def get_yt_info(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'No title')
        chapters = info.get('chapters', [])

        title_format = f"- YT: [{title}]({url})"

        if chapters:
            for c in chapters:
                c['start_time'] = seconds_to_time_format(c['start_time'])
                chapter_list = "\n- ".join([f"{c['start_time']} - {c['title']}" for c in chapters])
            chapter_list = f"- {chapter_list}"
        else:
            chapter_list = "No chapters available"

        # Copy chapter_list to clipboard using pbcopy
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        if chapter_list and chapter_list != "No chapters available":
            # # Copy the chapter_list to the clipboard if not empty
            # process.communicate(chapter_list.encode('utf-8'))
            # Copy the title + chapter_list to the clipboard if not empty
            process.communicate(
                f"{title_format}\n"
                f"### Chapters:\n"
                f"{chapter_list}".encode('utf-8')
            )
        else:
            # else copy title to clipboard
            process.communicate(title_format.encode('utf-8'))

        return (
            f"Title: {title}\n"
            f"{title_format}\n"
            f"### Chapters:\n"
            f"{chapter_list if chapter_list else 'No chapters available'}"
        )


if __name__ == '__main__':
    url = sys.argv[1]
    # url = "https://www.youtube.com/watch?v=WuitkfsqEoU"
    # url = "https://www.youtube.com/watch?v=HVTIQQXaClw"
    print(get_yt_info(url))
