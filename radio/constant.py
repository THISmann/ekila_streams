class RadioFluxRegex:
    SHOUCAST_REGEX = r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:\d{1,5})?/\w+$"
    ICECAST_REGEX = r"^(https?://)([a-zA-Z0-9.-]+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?(/[\w-./?%&=]*)?$"
    ECMANAGER_REGEX = r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}:\d{1,5}/\w+$"
    RCAST_REGEX = r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/\w+$"
    CENTOVACAST_REGEX = (
        r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:\d{1,5})?/[\w-]+/[\w-]+$"
    )
    AZURECAST_REGEX = r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[\w-]+/[\w.]+$"
    RADIOKING_REGEX = r"^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[\w-]+$"
