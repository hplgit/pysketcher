import os
from subprocess import Popen  # noqa: S404

EXAMPLE_DIR = "examples"


def main():
    files = [
        f
        for f in os.listdir(EXAMPLE_DIR)
        if os.path.isfile(os.path.join(EXAMPLE_DIR, f))
    ]

    def has_py_extension(filename: str) -> bool:
        _, ext = os.path.splitext(filename)
        return ext == ".py"

    examples = [f for f in files if has_py_extension(f)]
    os.chdir(EXAMPLE_DIR)
    for example in examples:
        proc = Popen(["python", example])  # noqa: S603,S607
        proc.wait()


if __name__ == "__main__":
    main()
