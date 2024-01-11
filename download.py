import gdown

url = "https://drive.google.com/file/d/1vobZ6KJZZQPh2RPJRgj3PwQpyLdPYKb-/view?usp=drive_link"
output = "best_model92.h5"
gdown.download(url, output, quiet=False, fuzzy=True, use_cookies=True)
