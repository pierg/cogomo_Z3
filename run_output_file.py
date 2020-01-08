import subprocess

with open("output.txt", "w+") as output:
    subprocess.call(["python3", "./evaluation/run_all.py"], stdout=output)
