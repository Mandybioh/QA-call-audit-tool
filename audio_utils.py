import os
from typing import Optional, Tuple, Union
import streamlit as st


def load_audio_bytes(audio_path: Union[str, bytes, bytearray, None]) -> Tuple[Optional[bytes], Optional[str]]:
    """Load audio bytes from a local file path or return a friendly error."""
    if audio_path is None:
        return None, "No audio path was provided."

    if isinstance(audio_path, (bytes, bytearray)):
        return bytes(audio_path), None

    if not isinstance(audio_path, str):
        audio_path = str(audio_path)

    if not audio_path:
        return None, "No audio path was provided."

    if not os.path.exists(audio_path):
        return None, f"Audio file was not found: {audio_path}"

    try:
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
    except (OSError, PermissionError, FileNotFoundError, ValueError) as exc:
        return None, f"Unable to read audio file: {exc}"

    if not audio_bytes:
        return None, "Audio file is empty."

    return audio_bytes, None


def render_audio_player(audio_path: Union[str, bytes, bytearray, None], *, label: Optional[str] = None) -> bool:
    """Render audio safely in Streamlit and return whether playback was displayed."""
    audio_bytes, error = load_audio_bytes(audio_path)
    if error:
        if label:
            st.warning(f"{label}: {error}")
        else:
            st.warning(error)
        return False

    file_ext = ""
    if isinstance(audio_path, str):
        file_ext = os.path.splitext(audio_path.lower())[1]

    content_type = "audio/wav"
    if file_ext == ".mp3":
        content_type = "audio/mpeg"
    elif file_ext == ".m4a":
        content_type = "audio/mp4"

    st.audio(audio_bytes, format=content_type)
    return True
