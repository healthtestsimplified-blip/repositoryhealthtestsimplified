import sys, os
T_DIR = os.path.dirname(os.path.abspath(__file__)); SITE_DIR = os.path.join(T_DIR, "..", "..", "site")
T = open(os.path.join(T_DIR, "template.html"), encoding="utf-8").read()
D = open(os.path.join(T_DIR, "data.js"), encoding="utf-8").read()
today = sys.argv[1] if len(sys.argv) > 1 else "thyroid"
out = (T.replace("{{DATA}}", D).replace("{{TODAY}}", today)
        .replace("{{FB}}", "https://www.facebook.com/profile.php?id=61594730205462")
        .replace("{{YT}}", "https://www.youtube.com/@Healthtestsimplified"))
open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8").write(out)
print("built, today =", today)
