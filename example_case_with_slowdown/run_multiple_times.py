import subprocess
import timeit


def run_pytest(number):
    subprocess.run(["pytest", "dir_0", "--collect-only"])


def make_directory(number):
    import os

    os.makedirs("./dir_0")
    for x in range(number):
        with open(f"dir_0/test_{x}.py", "w") as t:
            print("import pytest", file=t)
            print(f"def test_{x}():\n    pass", file=t)
            if x <= number:
                print(
                    f"""@pytest.fixture()
def fixture{x}():
    pass
            """,
                    file=t,
                )

    for root, dirs, files in os.walk("dir_0"):
        open(root + "/__init__.py", "w")


def setup(number):
    subprocess.run(["rm", "-rf", "dir_0"])
    make_directory(number)


with open("results.txt", "w") as results:
    for number in range(1, 10002, 500):
        time_taken = timeit.repeat(
            f"run_pytest({number})",
            globals=globals(),
            setup=f"setup({number})",
            number=1,
        )
        results.write(f"{number},{','.join(str(t) for t in time_taken)}\n")
        results.flush()
