def parse_http_request(reqstring: str) -> tuple[str, str] | None:
    first_line = reqstring.splitlines()[0].split(" ")

    if len(first_line) != 3:
        return None

    return first_line[0], first_line[1]
