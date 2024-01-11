import gdown

url = "https://drive.google.com/file/d/1TygrsDOY9UxAoBEd5pzfKEC82oyPimqT"
output = "best_model92.h5"
gdown.download(url, output, quiet=False, fuzzy=True)
