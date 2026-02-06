from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch
from transformers import AutoProcessor, VitsModel


@dataclass
class TTSConfig:
    model_id: str = "facebook/mms-tts"
    device: str = "cpu"
    language: str = "crk"


class TTSPipeline:
    def __init__(self, config: Optional[TTSConfig] = None) -> None:
        self.config = config or TTSConfig()
        self._processor = AutoProcessor.from_pretrained(self.config.model_id)
        self._model = VitsModel.from_pretrained(self.config.model_id).to(self.config.device)

    @property
    def sample_rate(self) -> int:
        return self._model.config.sampling_rate

    def synthesize(self, text: str, language: Optional[str] = None) -> torch.Tensor:
        lang = language or self.config.language
        inputs = self._processor(text, return_tensors="pt", language=lang)
        inputs = {k: v.to(self.config.device) for k, v in inputs.items()}
        with torch.no_grad():
            output = self._model(**inputs).waveform
        return output.squeeze(0).cpu()
