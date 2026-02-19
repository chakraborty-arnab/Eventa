import tempfile
from pathlib import Path

from faster_whisper import WhisperModel

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = WhisperModel("distil-large-v3", device="cpu", compute_type="int8")
    return _model


def transcribe(audio_bytes: bytes, filename: str = "audio.ogg") -> str:
    suffix = Path(filename).suffix or ".ogg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name

    segments, _ = _get_model().transcribe(tmp_path)
    Path(tmp_path).unlink(missing_ok=True)
    return " ".join(s.text for s in segments).strip()
