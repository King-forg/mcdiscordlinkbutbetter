"""Reads player chat out of a Minecraft server log."""

import re
from pathlib import Path


ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
CHAT_RE = re.compile(
    r"(?:^|(?:INFO|WARN)\]?:?\s*)"
    r"(?:\[Not Secure\]\s*)?"
    r"(?:\[[^\]\r\n]+\]\s*)*"
    r"<([^>\r\n]+)>\s?(.*)$"
)


class ChatLogTailer:
    def __init__(self, log_path):
        path = Path(log_path)
        # Accept either the folder (...\logs) or the file itself.
        if path.is_dir() or path.suffix == "":
            path = path / "latest.log"
        self.path = path
        self._pos = None
        self._buf = b""

    def read_new(self):
        """Return chat lines added since the last call without replaying old chat."""
        try:
            size = self.path.stat().st_size
        except FileNotFoundError:
            return []

        if self._pos is None:
            self._pos = size
            return []

        if size < self._pos:
            self._pos = 0
            self._buf = b""

        if size == self._pos:
            return []

        with self.path.open("rb") as log_file:
            log_file.seek(self._pos)
            data = log_file.read(size - self._pos)
        self._pos += len(data)

        lines = (self._buf + data).split(b"\n")
        self._buf = lines.pop()

        chats = []
        for raw in lines:
            line = ANSI_RE.sub("", raw.decode("utf-8", errors="replace")).rstrip("\r")
            match = CHAT_RE.search(line)
            if match:
                chats.append((match.group(1), match.group(2)))
        return chats
