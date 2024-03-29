from strenum import StrEnum


class SupportedAdapter(StrEnum):
    onebot_v11 = "OneBot V11"
    onebot_v12 = "OneBot V12"
    console = "Console"
    kaiheila = "Kaiheila"
    qqguild = "QQ Guild"
    telegram = "Telegram"
    feishu = "Feishu"
    red = "RedProtocol"
    discord = "Discord"
    villa = "Villa"
    dodo = "DoDo"


class SupportedPlatform(StrEnum):
    qq = "qq"
    console = "console"
    kaiheila = "kaiheila"
    qqguild = "qqguild"
    telegram = "telegram"
    feishu = "feishu"
    discord = "discord"
    villa = "villa"
    dodo = "dodo"
    unknown = "unknown"
