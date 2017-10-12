import os;
import time;
import zipfile
import shutil

dev = r"..\dev"						#relative to build.py
release = r"..\release"				#relative to build.py
pathToMonk = r"Jagent\Monk.jar"		#relative to build.py
readme = "readme.txt"				#relative to dev
versionfile = "version.txt"			#relative to build.py

releaseTemp = os.path.join(release, "temp")

with open(versionfile, 'r') as content_file:
	version = content_file.read()
print(version)

if os.path.exists(release):
	for root, dirs, files in os.walk(release):
		for f in files:
			os.unlink(os.path.join(root, f))
		for d in dirs:
			shutil.rmtree(os.path.join(root, d))
else:
	os.makedirs(release)

os.makedirs(releaseTemp)

for dirpath, dirnames, filenames in os.walk(dev):
	for filename in [f for f in filenames if f.endswith(".pray.cos")]:
		fullPathCos = os.path.join(dirpath, filename)
		print(fullPathCos)
		syatemArg = pathToMonk + " " + "\"" + fullPathCos + "\""
		os.system(syatemArg)
		for dirpath, dirnames, filenames in os.walk(dirpath):
			for filename in [f for f in filenames if f.endswith(".agents")]:
				fullPathAgent = os.path.join(dirpath, filename)
				newName = os.path.join(releaseTemp, filename)
				print(newName)
				if os.path.exists(newName):
					os.remove(newName)
				os.rename(fullPathAgent, newName)

readmeDestination = os.path.join(releaseTemp, readme)
print(readmeDestination)
if os.path.exists(readmeDestination):
	os.remove(readmeDestination)
print(os.path.join(dev, readme))
shutil.copyfile(os.path.join(dev, readme), readmeDestination)

shutil.make_archive(os.path.join(release, version), 'zip', releaseTemp)
shutil.rmtree(releaseTemp)

print("done")
#time.sleep(100)
