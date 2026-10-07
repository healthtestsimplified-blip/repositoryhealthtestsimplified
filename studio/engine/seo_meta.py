"""Embed SEO metadata (title, description, keywords) inside an MP4 without re-encoding.
Usage: python3 seo_meta.py video.mp4 "Title" "Description" "kw1, kw2, kw3"
"""
import os, subprocess, sys, json

def tag_video(path, title, description, keywords):
    tmp = path + ".tmp.mp4"
    md = {"title": title, "description": description, "synopsis": description, "comment": keywords,
          "keywords": keywords, "artist": "Health Test Simplified", "album_artist": "Health Test Simplified",
          "genre": "Health & Education", "copyright": "Health Test Simplified",
          "website": "https://healthtestsimplified.netlify.app"}
    args = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", path, "-map", "0", "-c", "copy"]
    for k, v in md.items(): args += ["-metadata", f"{k}={v}"]
    args += ["-movflags", "use_metadata_tags+faststart", tmp]
    subprocess.run(args, check=True); os.replace(tmp, path)
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format_tags", "-of", "json", path]).decode()
    return json.loads(out)["format"].get("tags", {})

if __name__ == "__main__":
    tags = tag_video(*sys.argv[1:5]); print({k: (v[:60] + "…" if len(v) > 60 else v) for k, v in tags.items()})
