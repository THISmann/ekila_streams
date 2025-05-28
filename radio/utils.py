from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    if url.endswith("/"):
        url = url[:-1]
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split(":")[0]
    if "http" in url:
        return f"http://{domain}"
    return f"https://{domain}"


def format_radio_king_radio_name(name: str) -> str:
    return name.lower().replace(" ", "-")


def remove_slash_on_uri(url: str) -> str:
    if url.endswith("/"):
        return url[:-1]
    return url


def normalize_uri_endpoint(url: str) -> str:
    if url.endswith("/"):
        return url
    return url + "/"
