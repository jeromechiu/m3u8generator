from pymediainfo import MediaInfo
import glob
import time
import os
import numpy as np

nginxPath = '/tmp/nginx/hls/'

def last_3chars(x):
	x = x.split('.ts')[0]
	return(x[-3:])

flushM3u8 = True
times = 0

def m3u8generator(files):
	global flushM3u8,times,nginxPath
	elmt = []

	files = sorted(files,key= last_3chars)[-3:]	
	print "Add %s to m3u8" %files
	for i in xrange(len(files)):
		files[i] = os.path.join(nginxPath, files[i])

	#print "files: %s" %files
	xMediaSequence = int(last_3chars(files[0].split('/')[-1]))
	
	print xMediaSequence
	for f in files:
		media_info = MediaInfo.parse(f)
		for track in media_info.tracks:
			if track.track_type == 'Video':
				#print f, track.bit_rate, track.bit_rate_mode, track.codec, track.duration
				elmt.append([f.split('/')[-1],float(track.duration)/1000])
	print "elmt: %s" %elmt

	print "%d times to attach payload" %times
	try:
		if flushM3u8:
			with open(os.path.join(nginxPath,'playlist.m3u8'),'w+') as f:
				content = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:%d\n#EXT-X-TARGETDURATION:1.9\n' %xMediaSequence
				f.write(content)
				f.write('#EXT-X-DISCONTINUITY\n')
				for l in elmt:
					f.write('#EXTINF:%f,\n%s\n' %(l[1],l[0]))
				#f.write('#EXT-X-ENDLIST')
				flushM3u8 = False
				times += 1
		else:
			buf = []
			with open(os.path.join(nginxPath,'playlist.m3u8'),'r+') as f:
				for line in f:
					if line != '#EXT-X-DISCONTINUITY\n':
						buf.append(line)
				f.seek(0)
				f.truncate()
				
				for i in buf:
					f.write(i)
				f.write('#EXT-X-DISCONTINUITY\n')
				
				for l in elmt:
					f.write('#EXTINF:%f,\n%s\n' %(l[1],l[0]))
				if times >= 4:
					flushM3u8 = True
					times = 0
				times += 1
			
	except IOError as e:
		print("Write File error: %s" %e)
		pass
	f.close()
	temp = np.asarray(elmt)
	
	return (np.sum(temp[:,1].astype(float), axis=0))
