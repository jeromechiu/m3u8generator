import os 
import shutil
import time
import glob
import m3u8Generator

localPath = './'
nginxPath = '/tmp/nginx/hls/'

def last_3chars(x):
	x = x.split('.ts')[0]
	return(x[-3:])
	
sourceFiles = filter(os.path.isfile, glob.glob(localPath+'*.ts'))
sourceFiles = sorted(sourceFiles,key= last_3chars)
print sourceFiles
numberofFile = len(sourceFiles)

count = 0
while True:
	
	for i in xrange(0,numberofFile,3):
		movedFiles = []
		try:
			deleteFiles = filter(os.path.isfile, glob.glob(nginxPath+'*.ts'))
			deleteFiles = sorted(deleteFiles,key= last_3chars)
			print "Total of files: %d" %len(deleteFiles)
			if len(deleteFiles) >= 25:
				for j in xrange(3):
					print "remove file: "+deleteFiles[j]
					os.remove(deleteFiles[j])
		except Exception as e:
			print "remove file error: %s" %e
		filename = "playlist_%010d.ts" %count
		destination = os.path.join(nginxPath, filename)
		shutil.copy(sourceFiles[i], destination)
		print "filename: %s" %filename
		movedFiles.append(filename)

		print "copy %s to destination" %destination
		count += 1
		#print "i=%d" %i
		i+=1
		if i <= numberofFile - 1:
			#print "i=%d,%d" %(i,numberofFile)
			filename = "playlist_%010d.ts" %count
			destination = os.path.join(nginxPath, filename)
			shutil.copy(sourceFiles[i], destination)
			print "filename: %s" %filename
			movedFiles.append(filename)
			print "copy %s to destination" %destination
			count += 1
			
		i += 1
		if i <= numberofFile - 1:
			#print "i=%d,%d" %(i,numberofFile)
			filename = "playlist_%010d.ts" %count
			destination = os.path.join(nginxPath, filename)
			shutil.copy(sourceFiles[i], destination)
			print "filename: %s" %filename
			movedFiles.append(filename)
			print "copy %s to destination" %destination
			count += 1
		
		if len(movedFiles):
			print "Ready moved %s" %movedFiles
			time.sleep(m3u8Generator.m3u8generator(movedFiles))
			
		print "done"