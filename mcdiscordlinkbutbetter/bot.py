from dataclasses import dataclass, field
from typing import Dict


@dataclass
class BotService:
    """Simple command service for linking Discord users to Minecraft usernames."""

    links: Dict[str, str] = field(default_factory=dict)
    linked_channels: Dict[str, str] = field(default_factory=dict)

    def link(self, discord_user_id: str, minecraft_username: str) -> str:
        self.links[discord_user_id] = minecraft_username
        return f"Linked {discord_user_id} to {minecraft_username}."

    def unlink(self, discord_user_id: str) -> str:
        removed = self.links.pop(discord_user_id, None)
        if removed is None:
            return f"No linked Minecraft account found for {discord_user_id}."
        return f"Unlinked {discord_user_id} from {removed}."

    def profile(self, discord_user_id: str) -> str:
        username = self.links.get(discord_user_id)
        if username is None:
            return f"{discord_user_id} is not linked yet."
        return f"{discord_user_id} is linked to {username}."

    def link_channel(self, guild_id: str, channel_id: str) -> str:
        self.linked_channels[guild_id] = channel_id
        return f"Guild {guild_id} linked to channel {channel_id}."

    def run_command(self, command: str, *args: str) -> str:
        handlers = {
            "link": self.link,
            "unlink": self.unlink,
            "profile": self.profile,
            "linkchannel": self.link_channel,
        }
        handler = handlers.get(command.lower())
        if handler is None:
            return "Unknown command. Available: link, unlink, profile, linkchannel"
        try:
            return handler(*args)
        except TypeError:
            return "Invalid command arguments."
