from k1lib.imports import *
from flask import Flask, request
app = Flask(__name__)

dbFn = "/data/lite.db"; dbInitialized = os.path.exists(dbFn)
lite = sql(dbFn, mode="lite")["default"]
if not dbInitialized:
    lite.query("""
CREATE TABLE calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    time BIGINT,
    headers TEXT,
    args TEXT,
    json TEXT
);""")
db = lite["calls"]

@app.route("/")
def index():
    catch_all("/"); ins = """
<h1>Webhook explorer</h1>
<p>This is a simple project aimed to listen to any incoming request on any
path and display out all info about them. This has been incredibly useful
for me to see what requests do other services and apis send back. You can
use this website as a public webhook explorer, and just send any requests
here, or if your data is sensitive, follow instructions on
<a href="https://github.com/157239n/webhook-explorer">https://github.com/157239n/webhook-explorer</a>
to set it up on your systems</p>
<button id="btnClear">Clear all requests</button>"""
    with k1.captureStdout() as out: db.info()
    h = '\n'.join(out()); overview = f"<pre>{html.escape(h)}</pre>"

    f = aS("f'/_control/page/{x}'") | aS(requests.get) | aS("x.text()") | aS(k1.resolve) | executeScriptTags()
    ui = range(20) | (toJsFunc() | apply(viz.onload() | f) | viz.Carousel()) | op().interface() | toHtml()
    return f"""{ins}<h1>Sqlite database overview</h1>{overview}<h1>Recent requests</h1>{ui}
<script>document.querySelector("#btnClear").onclick = async () => {{ await fetch("/_control/wipe"); location.reload(); }}</script>"""

@app.route("/_control/overview")
def control_overview():
    with k1.captureStdout() as out: db.info()
    h = '\n'.join(out())
    return f"<pre>{html.escape(h)}</pre>"

@app.route("/_control/wipe")
def control_wipe(): lite.query("""DELETE FROM calls"""); return f"ok"

@app.route("/_control/page/<int:i>")
def control_page(i):
    res = db.query(f"select id, path, time, headers, args, json from calls order by rowid desc limit 30 offset ?", int(i)*30) | apply(lambda row: [*row[:3], *row[2:]]) | apply(toIso(), 3) | apply(tryout() | aS(json.loads), [4,5])
    h = res | viz.Table(["idx", "path", "unix time", "utc time", "headers", "args", "json"], ondeleteFName="deleteF", colOpts=[[], [], [], [], ["json", "clipboard"], ["json", "clipboard"], ["json", "clipboard"]])
    return f"""
<script>
async function deleteF(row, i, e) {{
    const res = await fetch(`/_control/remove/${{row[0]}}`);
    if (!res.ok) throw new Error(`${{res.body}}`)
}}
</script>
{h}"""

@app.route("/_control/remove/<int:idx>")
def control_remove(idx): del db[idx]; return "ok"

@app.route("/<path:path>")
def catch_all(path):
    try: js = request.json
    except: js = None
    headers = json.dumps({e.split(":")[0]:":".join(e.split(":")[1:]).strip() for e in f"{request.headers}".replace("\r", "").strip().split("\n")})
    db.insert(path=path, time=time.time(), headers=headers, args=json.dumps(request.values), json=(None if js is None else f"{js}"))
    return "recorded"

app.run(host="0.0.0.0", port=80)


