"""Hindi teaser for a Bengali genetics episode: first K scenes of the episode + 'watch the full video' end card,
voiced by Swara (python3 hi_swara.py <id>t first). Usage: python3 hindi_teaser.py g010 4 "End-card question"."""
import importlib, sys
from cbc_cartoon import run
from hts_close import close_scene
import doc_style

k, n, q = sys.argv[1], int(sys.argv[2]), sys.argv[3]
m = importlib.import_module(k)
SC = list(m.SC[:n]) + [(close_scene(q, "WATCH THE FULL VIDEO ON OUR CHANNEL"), "docl")]
run(SC, f"/tmp/{k}t_", f"/tmp/hts-{k}-teaser-hi.mp4", max_sec=180)
