from __future__ import annotations

import base64
import io
import wave
from typing import Optional

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.cap import CAPAlert
from app.tts import TTSConfig, TTSPipeline

app = FastAPI(title="Plains Cree MMS TTS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = TTSPipeline(TTSConfig())


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1)
    language: Optional[str] = Field(default=None, description="MMS language code, e.g. crk.")
    cap: Optional[CAPAlert] = Field(default=None, description="CAP metadata block.")


class TTSResponse(BaseModel):
    audio_wav_base64: str
    sample_rate: int
    cap: Optional[CAPAlert]


def _to_wav_bytes(audio: np.ndarray, sample_rate: int) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    return buffer.getvalue()


@app.post("/api/tts", response_model=TTSResponse)
async def synthesize_tts(request: TTSRequest) -> TTSResponse:
    waveform = pipeline.synthesize(request.text, request.language)
    audio_int16 = (waveform.numpy() * 32767).astype(np.int16)
    wav_bytes = _to_wav_bytes(audio_int16, pipeline.sample_rate)
    audio_b64 = base64.b64encode(wav_bytes).decode("utf-8")
    return TTSResponse(audio_wav_base64=audio_b64, sample_rate=pipeline.sample_rate, cap=request.cap)


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
