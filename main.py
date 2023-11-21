from pytube import YouTube
import pytube.exceptions
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import art


def content_details(details: YouTube):
    print(f"Title: {details.title}")


def download_message(filename):
    print(f"Downloading {filename}")


def choose_quality(yt: YouTube, audio=False):
    content_list = []

    if not audio:
        print("Index\tResolution\tCodecs")
        for i, stream in enumerate(
            yt.streams.filter(only_video=True).order_by("resolution").desc(), start=1
        ):
            content_list.append(stream)
            print(f"{i}\t{stream.resolution}\t\t{' '.join(stream.codecs)}")
    else:
        print("Index\tQuality\t\tCodecs")
        for i, stream in enumerate(
            yt.streams.filter(only_audio=True).order_by("abr").desc(), start=1
        ):
            content_list.append(stream)
            print(f"{i}\t{stream.abr}\t\t{' '.join(stream.codecs)}")

    idx = int(input("Enter an index: ")) - 1

    if 0 <= idx < len(content_list):
        if not audio:
            video_download(
                content_list[idx],
                filename=f"{yt.title}{content_list[idx].resolution}",
                yt=yt,
            )
        else:
            audio_downloader(
                content_list[idx], filename=f"{yt.title}{content_list[idx].abr}"
            )
    else:
        print("Sorry!! You chose the wrong index!!")


def audio_downloader(stream, filename: str):
    download_message(filename=filename)
    stream.download(filename=filename)

    mp4_file = filename
    mp3_file = f"{os.path.splitext(filename)[0]}.mp3"

    audio_clip = AudioFileClip(mp4_file)
    audio_clip.write_audiofile(mp3_file)

    os.remove(mp4_file)


def audio_download(stream, filename: str):
    download_message(filename=filename)
    stream.download(filename=filename)


def video_download(stream, filename: str, yt: YouTube):
    download_message(filename=filename)

    audio_streams = yt.streams.filter(only_audio=True).order_by("abr").desc()

    if audio_streams:
        temp_audio_stream = audio_streams[0]
        temp_audio_filename = f"{yt.title}_temp_audio"
        audio_download(temp_audio_stream, filename=temp_audio_filename)
        temp_audio = AudioFileClip(temp_audio_filename)
    else:
        print("No audio streams available. Downloading video without audio.")
        temp_audio = None

    stream.download(filename=filename)

    if temp_audio:
        try:
            video_clip = VideoFileClip(filename)
            audio_clip = temp_audio

            final_clip = video_clip.set_audio(audio_clip)

            title = input("Enter a title: ")

            final_clip.write_videofile(title + ".mp4")

        except IndexError:
            print(
                "Error: Cannot merge audio and video. No audio information in the video stream."
            )
        os.remove(temp_audio_filename)
        os.remove(filename)


if __name__ == "__main__":
    try:
        print(art.logo)
        link: str = input("Enter the Youtube Link : ")
        yt_link = YouTube(link)
        content_details(yt_link)
        choice: int = int(input("What You Want to Download\n1. Video\n2. Audio")) - 1
        choose_quality(yt_link, audio=bool(choice))
    except pytube.exceptions.RegexMatchError:
        print("Sorry!! Invalid Link!!")
