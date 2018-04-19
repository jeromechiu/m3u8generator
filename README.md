# m3u8generator
This is python code for live stream media server to run as HLS service. The program scans specific folder to get file list which list new uploaded video chunk file. The duration of every chunk video file is 1 second. Architecure likes as

chunk<--upload-->m3u8generator<--copy video/m3u8 to web server-->webserver<---->hls player
