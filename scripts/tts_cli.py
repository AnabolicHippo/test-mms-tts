from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

import soundfile as sf

from app.cap import CAPAlert
from app.tts import TTSConfig, TTSPipeline


def _load_cap(cap_path: Optional[Path]) -> Optional[CAPAlert]:
    if not cap_path:
        return None
    data = json.loads(cap_path.read_text())
    return CAPAlert.model_validate(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MMS TTS audio for Plains Cree.")
    parser.add_argument("text", help="Text to synthesize.")
    parser.add_argument("--output", "-o", default="output.wav", help="Output WAV path.")
    parser.add_argument("--language", "-l", default="crk", help="MMS language code.")
    parser.add_argument("--cap", type=Path, help="Optional CAP metadata JSON file.")
    args = parser.parse_args()

    pipeline = TTSPipeline(TTSConfig(language=args.language))
    waveform = pipeline.synthesize(args.text, args.language)
    sf.write(args.output, waveform.numpy(), pipeline.sample_rate)

    cap = _load_cap(args.cap)
    if cap:
        cap_output = Path(args.output).with_suffix(".cap.json")
        cap_output.write_text(cap.model_dump_json(indent=2, by_alias=True))


if __name__ == "__main__":
    main()
