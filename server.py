import os
import requests
from flask import Flask, Response, abort

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Config — set these as environment variables in Railway, never hardcode them
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")   # your classic PAT
GITHUB_USER  = os.environ.get("GITHUB_USER")    # your GitHub username
GITHUB_REPO  = os.environ.get("GITHUB_REPO")    # your repo name  e.g. "boost-lua"
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "main")

# Optional: a secret key callers must pass so randos can't hit your server
SERVER_KEY = os.environ.get("SERVER_KEY")        # leave blank to disable check

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def fetch_from_github(path: str) -> str:
    """Fetch any file from the private repo using the stored token."""
    url = (
        f"https://raw.githubusercontent.com"
        f"/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"
    )
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(url, headers=headers, timeout=10)

    if resp.status_code == 404:
        abort(404, description=f"File not found in repo: {path}")
    if resp.status_code != 200:
        abort(502, description=f"GitHub returned {resp.status_code}")

    return resp.text

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return "boost.lua server is running.", 200


@app.route("/script")
def serve_script():
    """
    Main endpoint — returns boost.lua so the executor can loadstring it.
    Optional header check: X-Key: <SERVER_KEY>
    """
    if SERVER_KEY:
        provided = request_key()
        if provided != SERVER_KEY:
            abort(403, description="Invalid key.")

    lua = fetch_from_github("boost.lua")
    return Response(lua, mimetype="text/plain")


@app.route("/script/<path:filepath>")
def serve_file(filepath):
    """
    Serve any other .lua file from the repo by path.
    e.g. GET /script/modules/utils.lua
    """
    if SERVER_KEY:
        provided = request_key()
        if provided != SERVER_KEY:
            abort(403, description="Invalid key.")

    if not filepath.endswith(".lua"):
        abort(400, description="Only .lua files are served.")

    lua = fetch_from_github(filepath)
    return Response(lua, mimetype="text/plain")


# ---------------------------------------------------------------------------
# Internal
# ---------------------------------------------------------------------------

def request_key():
    from flask import request
    # Accept key from header OR query param
    return request.headers.get("X-Key") or request.args.get("key", "")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
