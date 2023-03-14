import io
import subprocess
import multiprocessing.pool
from datetime import datetime

def check_guess(guess):
    # setsid to create a new session and detach from the current tty
    # sudo likes to print directly to the tty, bypassing stdout/stderr
    process = subprocess.Popen(
        ["setsid", "bash", "-c", "sudo -S -k echo -n hi"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    stdout, stderr = process.communicate(guess.encode("utf-8"))

    return stdout.decode("utf-8") == "hi"

def generate_guesses():
    process = subprocess.Popen(
        ["../john/run/john", "--wordlist=base.txt", "--rules", "--stdout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
        yield line

start = datetime.now()
n_guesses = 0

guesses = list(generate_guesses())
total_guesses = len(guesses)

print("Total candidates:", total_guesses)

pool = multiprocessing.pool.ThreadPool(200)
found = False

def worker(guess):
    global n_guesses
    global found
    if found:
        # Easiest way I can find to wrap up the pool
        return
    n_guesses += 1
    if n_guesses % 1000 == 0:
        # guesses / second
        elapsed_time = (datetime.now() - start).total_seconds()
        guess_rate = n_guesses / elapsed_time
        print(f"{n_guesses} guesses - {((total_guesses - n_guesses) / guess_rate) / 60:.2f} minutes remaining")
    if check_guess(guess):
        print("Found it:", guess)
        found = True

pool.map(worker, guesses)
