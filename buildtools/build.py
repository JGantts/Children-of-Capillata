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

FileTypesToParse= (".txt",".cos",".pray.cos", ".catalogue")

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

	#clear out or make release folder
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
		if(len(filenames)!=0):
			print("Processing " + os.path.join(dirpath))
# Replace all ReSTing's (Replacement System Thing piece of text) with their parsed outputs.
# For example:
	#[[<[[Format: version, vA.B|vA.B.C.D-T]]>]]
#	may become
#	v1.3
#	or
#	V1.3.0.1-alpha
		for filename in [f for f in filenames if f.endswith(FileTypesToParse)]:
			fullPathFile = os.path.join(dirpath, filename)
			print("Backing up " + fullPathFile)

			with open(fullPathFile, 'r+') as f:
				text = f.read()
# Make backup of original file
				with open(fullPathFile + ".bak", 'w') as backupFile:
					backupFile.write(text)

				f.seek(0)
				f.write(Parser.parseAndReplace(text))
				f.truncate()

		for filename in [f for f in filenames if f.endswith(".pray.cos")]:
# Package using Monk
			fullPathCos = os.path.join(dirpath, filename)
			print("Packaging  " + fullPathCos)
			syatemArg = PathToMonk + " " + "\"" + fullPathCos + "\""
			os.system(syatemArg)
			for dirpath, dirnames, filenames in os.walk(dirpath):
				for filename in [f for f in filenames if f.endswith(".agents")]:
# Moving the .agents to the releaseTemp folder
					fullPathAgent = os.path.join(dirpath, filename)
					newName = os.path.join(ReleaseTemp, filename)
					print("Moving     " + newName)
					if os.path.exists(newName):
						os.remove(newName)
					os.rename(fullPathAgent, newName)
		if(len(filenames)!=0):
			print("End        " + os.path.join(dirpath), end="\n\n")

	#	Copy the readme
	readmeDestination = os.path.join(ReleaseTemp, Readme)
	print("\nCopying    " + readmeDestination)
	if os.path.exists(readmeDestination):
		os.remove(readmeDestination)
	shutil.copyfile(os.path.join(Dev, Readme), readmeDestination)

	#	Zip up files
	zipFile = os.path.join(Release, Formatter.getFormat("version", "N vW.X|vW.X.Y.Z-T"))
	print("Zipping    " + zipFile + ".zip")
	shutil.make_archive(zipFile, 'zip', ReleaseTemp)
	shutil.rmtree(ReleaseTemp)

# Replace original files with backups
	print("")
	for dirpath, dirnames, filenames in os.walk(Dev):
		for filename in [f for f in filenames if f.endswith(".bak")]:
			fullPathFileWithBak = os.path.join(dirpath, filename)
			fullPathFileNoBak = fullPathFileWithBak.replace(".bak", "")
			print("Deleting   " + fullPathFileWithBak)
			os.remove(fullPathFileNoBak)
			os.rename(fullPathFileWithBak, fullPathFileNoBak)

class Parser():
	@staticmethod
	def parseAndReplace(fileIn):
		index = 0
		state = 0
		restingStart = -1
		lastRestingEnd = -1
		fileOutChunked = []
# We're looking for strings like "[[<[[blah blah blah]]>]]"
# The state variable stores how far we've gotten:
# 0		Looking for `[`[<[[    ]]>]]
# 1		Looking for [`[`<[[    ]]>]]
# 2		Looking for [[`<`[[    ]]>]]
# 3		Looking for [[<`[`[    ]]>]]
# 4		Looking for [[<[`[`    ]]>]]
# 5		Looking for   [[<[[    `]`]>]]
# 6		Looking for   [[<[[    ]`]`>]]
# 7		Looking for   [[<[[    ]]`>`]]
# 8		Looking for   [[<[[    ]]>`]`]
# 9		Looking for   [[<[[    ]]>]`]`
		while index < len(fileIn):
			if(state==0):
				if(fileIn[index]=='['):
					state = 1
			elif(state==1):
				if(fileIn[index]=='['):
					state = 2
				else:
					state = 0
			elif(state==2):
				if(fileIn[index]=='<'):
					state = 3
				else:
					state = 0
			elif(state==3):
				if(fileIn[index]=='['):
					state = 4
				else:
					state = 0
			elif(state==4):
				if(fileIn[index]=='['):
					state = 5
					restingStart = index - 4
# We found an opening [[<[[
#	Save everything up till here for file output
					fileOutChunked += fileIn[lastRestingEnd+1:restingStart]
				else:
					state = 0
			elif(state==5):
				if(fileIn[index]==']'):
					state = 6
			elif(state==6):
				if(fileIn[index]==']'):
					state = 7
				else:
					state = 5
			elif(state==7):
				if(fileIn[index]=='>'):
					state = 8
				else:
					state = 5
			elif(state==8):
				if(fileIn[index]==']'):
					state = 9
				else:
					state = 5
			else:
				if(fileIn[index]==']'):
# We found a closing ]]>]]
					state = 0
					lastRestingEnd = index
					fileOutChunked += Parser.parseResting(fileIn, restingStart, index)
				else:
					state = 5
			index = index+1
		if( state > 4):
			assert(False, "Error: Found opening [[<[[ but no closing ]]>]].")
#	Save everything else for file output
		fileOutChunked += fileIn[lastRestingEnd+1:index]
		return(''.join(fileOutChunked))

	@staticmethod
	def parseResting(fileIn, startIndex, endIndex):
		#resting = fileIn[startIndex:endIndex+1]
		resting = fileIn[startIndex+5:endIndex-4]
		commandEnd = str.find(resting, ':')
		command = resting[:commandEnd]
		arguments = resting[commandEnd+1:].split(",")
		arguments = filter(None, arguments)
		argumentsList = list(map(str.strip, arguments))
		if(command.upper() == "FORMAT"):
			toReturn = Formatter.getFormat(argumentsList[0], argumentsList[1])
		else:
			toReturn = ""
		return toReturn

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
					"v" +
					VersionArray[0] +
					"." +
					VersionArray[1] +
					"." +
					VersionArray[2] )
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
