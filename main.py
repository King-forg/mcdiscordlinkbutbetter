from mcdiscordlinkbutbetter import BotService


def main() -> None:
    service = BotService()
    print(service.run_command("link", "discord-user-1", "Steve"))
    print(service.run_command("profile", "discord-user-1"))


if __name__ == "__main__":
    main()
