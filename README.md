# Sudo Guesser

This script brute forces sudo password guesses. By default it generates guesses using [john the ripper][j].

Motivation: I forgot my password to a system I didn't have physical access to after a month of not typing it, but I had
a rough idea of what it was.

How to use:
- Configure and build john the ripper
- Populate `base.txt` with your guesses for the password (this script invokes john with --rules so john will generate
  variations)
- Update the path to the john binary in the script

If the script finds the password it will be printed to stdout.

Sudo introduces a delay after an incorrect password guess is made at least in part to mitigate brute force attacks. This
mitigation is bypassed by simply launching hundreds of sudo processes in parallel. By default this script uses a python
multiprocessing pool of 200 workers.

[j]: https://github.com/openwall/john
