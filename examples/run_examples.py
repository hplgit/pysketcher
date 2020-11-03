import os
from subprocess import Popen

EXAMPLE_DIR = "."


class BColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END_COLOR = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


skip_list = [
    "comprehensive_rectangles.py",
    "flow_over_gaussian.py",
    "integral_comic_strip.py",
    "oscillator_sketch1.py",
    "oscillator_sketch2.py",
    "pendulum2.py",
    "ForwardEuler_comic_strip.py",
]


def main():
    files = [
        f
        for f in os.listdir(EXAMPLE_DIR)
        if os.path.isfile(os.path.join(EXAMPLE_DIR, f))
    ]

    def has_py_extension(filename: str) -> bool:
        _, ext = os.path.splitext(filename)
        return ext == ".py"

    examples = [f for f in files if has_py_extension(f) and f != __file__]
    os.chdir(EXAMPLE_DIR)
    for example in examples:
        if example in skip_list:
            continue
        print(f"{BColors.OKGREEN}Running {example}.{BColors.END_COLOR}")
        proc = Popen(["python", example])
        proc.wait()


if __name__ == "__main__":
    main()
