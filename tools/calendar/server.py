#!/usr/bin/env python3
"""
Dolmenwood Calendar – sync server.
Provides a state API so all players see the same calendar date/weather
set by the Referee. Static files are served by Cytrus/nginx separately.

Endpoints:
  GET  /api/state       – return current state JSON (public)
  POST /api/state       – update state (requires X-Referee-Token header)

Environment variables (set in .env):
  REFEREE_TOKEN   – secret token Referee must supply to POST state
  PORT            – port to listen on (default: 3000)
  ALLOWED_ORIGIN  – CORS allowed origin (default: https://edrache.cytr.us)
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response

load_dotenv(Path(__file__).parent / ".env")

REFEREE_TOKEN = os.environ.get("REFEREE_TOKEN", "")
PORT = int(os.environ.get("PORT", 3000))
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://edrache.cytr.us")
BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / "state.json"

DEFAULT_STATE = {
    "month": 1,
    "day": 1,
    "year": 1,
    "weatherText": "",
    "weatherFlags": {"I": False, "V": False, "W": False},
    "publicNote": "",
    "yearLabel": "",
}

app = Flask(__name__)


def cors(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Referee-Token"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.after_request
def add_cors(response):
    return cors(response)


def load_state() -> dict:
    try:
        if STATE_FILE.exists():
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            merged = {**DEFAULT_STATE, **data}
            merged["weatherFlags"] = {**DEFAULT_STATE["weatherFlags"], **merged.get("weatherFlags", {})}
            return merged
    except Exception:
        pass
    return dict(DEFAULT_STATE)


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


@app.route("/api/state", methods=["OPTIONS"])
def state_options():
    return make_response("", 204)


@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(load_state())


@app.route("/api/state", methods=["POST"])
def set_state():
    if not REFEREE_TOKEN:
        return jsonify({"error": "Server misconfigured: REFEREE_TOKEN not set"}), 500

    token = request.headers.get("X-Referee-Token", "")
    if token != REFEREE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        new_state = request.get_json(force=True)
        if not isinstance(new_state, dict):
            raise ValueError("Expected JSON object")
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {e}"}), 400

    merged = {**DEFAULT_STATE, **new_state}
    merged["weatherFlags"] = {**DEFAULT_STATE["weatherFlags"], **merged.get("weatherFlags", {})}

    save_state(merged)
    return jsonify({"ok": True})


if __name__ == "__main__":
    if not REFEREE_TOKEN:
        print(
            "WARNING: REFEREE_TOKEN is not set. "
            "Copy .env.example to .env and set a secret token.",
            file=sys.stderr,
        )
    print(f"Starting Dolmenwood Calendar API on http://0.0.0.0:{PORT}")
    print(f"  API endpoint: http://localhost:{PORT}/api/state")
    print(f"  CORS origin:  {ALLOWED_ORIGIN}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
