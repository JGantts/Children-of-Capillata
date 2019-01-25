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

#read in version from versionFile
with open(versionfile, 'r') as content_file:
	version = content_file.readline().rstrip()
print("Building " + version)

#clear out or make release file
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
#	Package using Monk
		fullPathCos = os.path.join(dirpath, filename)
		print("Packaging " + fullPathCos)
		syatemArg = pathToMonk + " " + "\"" + fullPathCos + "\""
		os.system(syatemArg)
		for dirpath, dirnames, filenames in os.walk(dirpath):
			for filename in [f for f in filenames if f.endswith(".agents")]:
#	Moving the .agents to the releaseTemp folder
				fullPathAgent = os.path.join(dirpath, filename)
				newName = os.path.join(releaseTemp, filename)
				print("Moving    " + newName)
				if os.path.exists(newName):
					os.remove(newName)
				os.rename(fullPathAgent, newName)
#	Copy the readme
readmeDestination = os.path.join(releaseTemp, readme)
print("Copying   " + readmeDestination)
if os.path.exists(readmeDestination):
	os.remove(readmeDestination)
shutil.copyfile(os.path.join(dev, readme), readmeDestination)

#	Zip up files
zipFile = os.path.join(release, version)
print("Zipping   " + zipFile + ".zip")
shutil.make_archive(zipFile, 'zip', releaseTemp)
shutil.rmtree(releaseTemp)

print("done")
#time.sleep(100)
