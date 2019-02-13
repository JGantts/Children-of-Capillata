import os;
import time;
import zipfile
import shutil
import traceback

Dev = r"..\dev"						#relative to build.py
Release = r"..\release"				#relative to build.py
PathToMonk = r"Jagent\Monk.jar"		#relative to build.py
Readme = "readme.txt"				#relative to dev
Versionfile = "version.txt"			#relative to build.py

FileTypesToParse= [".txt",".cos",".pray.cos"]

ReleaseName = "Children of Capillata"

ReleaseTemp = os.path.join(Release, "temp")
VersionArray = ["0", "0", "0", "0"]

def main():
	#read in version from versionFile, update it, and save it to versionFile
	with open(Versionfile, 'r+') as f:
		versionFileLineOld = f.readline().rstrip()
	#Find last build number and add 1 to it
		versionArrayOld = versionFileLineOld.split(".")
		assert(len(versionArrayOld) == 4)
		assert(versionArrayOld[0].isdigit())
		assert(versionArrayOld[1].isdigit())
		assert(versionArrayOld[2].isdigit())
		assert(versionArrayOld[3].isdigit()
			or versionArrayOld[3]=="-1"
			or versionArrayOld[3]=="x")
		oldBuildNumber = versionArrayOld[3]
		if(oldBuildNumber.isdigit() or oldBuildNumber=="-1"):
			newBuildNumber = str(int(oldBuildNumber) + 1)
		else:
# Uninitialized repo clone. Start at 1
			newBuildNumber = "1"
		versionArrayOld[3] = newBuildNumber
		global VersionArray
		VersionArray = versionArrayOld
		versionFileLineNew = '.'.join(VersionArray)
	#Save new version
		f.seek(0)
		f.write(versionFileLineNew + "\n")
		f.truncate()

	print("Building " + versionFileLineNew)
	print("         " + Formatter.getFormat("version", "vW.X|vW.X.Y|vW.X.Y.Z"))
	print("         " + Formatter.getFormat("version", "vW.X|vW.X.Y.Z-T"))
	print("         " + Formatter.getFormat("version", "N vW.X|vW.X.Y.Z-T"))
	print("")

	#clear out or make release file
	if os.path.exists(Release):
		for root, dirs, files in os.walk(Release):
			for f in files:
				os.unlink(os.path.join(root, f))
			for d in dirs:
				shutil.rmtree(os.path.join(root, d))
	else:
		os.makedirs(Release)
	os.makedirs(ReleaseTemp)

	for dirpath, dirnames, filenames in os.walk(Dev):
		#for filename in [f for f in filenames if f.endswith(FileTypesToParse)]:


		for filename in [f for f in filenames if f.endswith(".pray.cos")]:
	#	Package using Monk
			fullPathCos = os.path.join(dirpath, filename)
			print("Packaging " + fullPathCos)
			syatemArg = PathToMonk + " " + "\"" + fullPathCos + "\""
			os.system(syatemArg)
			for dirpath, dirnames, filenames in os.walk(dirpath):
				for filename in [f for f in filenames if f.endswith(".agents")]:
	#	Moving the .agents to the releaseTemp folder
					fullPathAgent = os.path.join(dirpath, filename)
					newName = os.path.join(ReleaseTemp, filename)
					print("Moving    " + newName)
					if os.path.exists(newName):
						os.remove(newName)
					os.rename(fullPathAgent, newName)
	#	Copy the readme
	readmeDestination = os.path.join(ReleaseTemp, Readme)
	print("Copying   " + readmeDestination)
	if os.path.exists(readmeDestination):
		os.remove(readmeDestination)
	shutil.copyfile(os.path.join(Dev, Readme), readmeDestination)

	#	Zip up files
	zipFile = os.path.join(Release, Formatter.getFormat("version", "N vW.X|vW.X.Y.Z-T"))
	print("Zipping   " + zipFile + ".zip")
	shutil.make_archive(zipFile, 'zip', ReleaseTemp)
	shutil.rmtree(ReleaseTemp)

class Formatter():
	types = ["version", "date"]

	class ReleaseType():
		FULL = 0  # 1.0|1.1 Regular release
		BETA = 1  # 1.1.1   Beta test release
		ALPHA = 2 # 1.1.1.1 Alpha test (maybe release)

	@staticmethod
	def validType(value):
		assert(isinstance(value, str))
		return any(type == value for type in Formatter.types)

	@classmethod
	def getFormat(cls, formatType, formatArgment):
		assert(Formatter.validType(formatType))
		assert(isinstance(formatArgment, str))

		if( VersionArray[3]!="0" ):
# x.x.x.1
			type = cls.ReleaseType.ALPHA
		elif( VersionArray[2]!="0" ):
# x.x.1.0
			type = cls.ReleaseType.BETA
		else:
# x.x.0.0
			type = cls.ReleaseType.FULL

		toReturn = ""
# BEGIN -Garbage which needs to be replaced.
		if(formatArgment == "vW.X|vW.X.Y.Z-T"):
			if(type == cls.ReleaseType.FULL):
				toReturn = (
					"v" +
					VersionArray[0] +
					"." +
					VersionArray[1] )
			else:
				toReturn = (
					"v" +
					VersionArray[0] +
					"." +
					VersionArray[1] +
					"." +
					VersionArray[2] +
					"." +
					VersionArray[3] )
				if(type == cls.ReleaseType.BETA):
					toReturn += "-beta"
				else:
					toReturn += "-alpha"
		elif(formatArgment == "vW.X|vW.X.Y|vW.X.Y.Z"):
			if(type == cls.ReleaseType.FULL):
				toReturn = (
					"v" +
					VersionArray[0] +
					"." +
					VersionArray[1] )
			elif(type == cls.ReleaseType.BETA):
					toReturn = (
					VersionArray[0] +
					"." +
					VersionArray[1] +
					"." +
					VersionArray[2] )
			else:
					toReturn = (
					VersionArray[0] +
					"." +
					VersionArray[1] +
					"." +
					VersionArray[2] +
					"." +
					VersionArray[3] )
		elif(formatArgment == "N vW.X|vW.X.Y.Z-T"):
			if(type == cls.ReleaseType.FULL):
				toReturn = (
					ReleaseName +
					" v" +
					VersionArray[0] +
					"." +
					VersionArray[1] )
			else:
				toReturn = (
					"v" +
					VersionArray[0] +
					"." +
					VersionArray[1] +
					"." +
					VersionArray[2] +
					"." +
					VersionArray[3] )
				if(type == cls.ReleaseType.BETA):
					toReturn += "-beta"
				else:
					toReturn += "-alpha"
		else:
			assert(False)
# END -Garbage which needs to be replaced.
# -Jacob Gantt 2019/2/13
		return toReturn

try:
	main()
	print("\n\ndone.")
	print("(5 seconds...)")
	time.sleep(5)
except Exception as e:
	print("\n\nError, build failed:\n\n" + str(e) + "\n\n")
	print(traceback.format_exc())
	print("\n\ndone.")
	input("Press any key to exit.")
