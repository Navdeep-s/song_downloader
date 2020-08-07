import os
y= input("path of the files to be downloaded")

if os.path.exists(y):
	k = open("path.txt","w+")
	k.write(y)
	k.close()
else:
	print("please check if the path exist")

os.chdir(y)
k = open("current_song","w+")
k.write("1")
k.close()

print("initializing complete")
