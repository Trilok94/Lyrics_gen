import os

file_names = [f.replace(".txt", "") for f in os.listdir(".") if f.endswith(".txt")]
print(file_names)
