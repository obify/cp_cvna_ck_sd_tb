# Python program to explain os.mkdir() method

# importing os module
import os

# Directory
directory = "Lecture-"

# Parent Directory path
parent_dir = "E:/HARD-DISK/Ranjan Udemy Final/Obify/Develop & Deploy Java Springboot App on Kubernetes Cluster/"

# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
for i in range(30,38):
    # Path
    path = os.path.join(parent_dir, directory+str(i))
    os.mkdir(path)

print("Directory '% s' created" % directory)

