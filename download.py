import gdown

url = "1vobZ6KJZZQPh2RPJRgj3PwQpyLdPYKb-"
output = "best_model92.h5"
gdown.download(url, output, quiet=False, fuzzy=True, use_cookies=True)
