import os
import atexit
import subprocess

def install_playwright_chromium():
	python_path = os.path.join("..", "..", "env", "bin", "python")
	print(subprocess.run(f"{python_path} -m playwright install chromium", shell=True))

def setup():
	atexit.register(install_playwright_chromium)

