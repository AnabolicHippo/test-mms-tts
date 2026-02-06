# Plains Cree MMS TTS

This project provides a command-line tool and a small web interface for generating Plains Cree
text-to-speech audio using the [facebook/mms-tts](https://huggingface.co/facebook/mms-tts) model.
It also supports attaching Common Alerting Protocol (CAP) metadata for emergency messaging.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI Usage

```bash
python scripts/tts_cli.py "tânisi" --output tts.wav --language crk
```

Add CAP metadata by pointing to a JSON file:

```bash
python scripts/tts_cli.py "alert" --cap cap.json
```

When a CAP file is provided, a sidecar `*.cap.json` file is saved next to the audio output.

## Web App

Start the API + frontend:

```bash
uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000 to submit text and CAP metadata, generate audio, and preview it
in the embedded player.
