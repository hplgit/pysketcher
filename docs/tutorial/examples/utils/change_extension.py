import os


def change_extension(filename: str, extension: str) -> str:
    name, path = os.path.splitext(filename)
    return f"{name}.{extension}"
