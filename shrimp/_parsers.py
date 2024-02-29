def parse_http_request(reqstring: str) -> tuple[str, str] | None:
    """Parses an HTTP request string and returns a tuple containing the method and route

    ## Arguments:
        `reqstring` (`str`): The HTTP request string

    ## Returns:
        `tuple[str, str] | None`: Method and route or none if the reqstring is invalid
    """

    first_line = reqstring.splitlines()[0].split(" ")

    if len(first_line) != 3:
        return None

    return first_line[0], first_line[1]
