# Audio-Chunking-Tool
An audio tool using pydubs library with python to chunk your audio content into your desired length, and parameters to tune. 
To run this script just type this in your terminal:

python3 mp3_chunk.py --path Data_Test/RL3 --boc-path boc2 --chunk-length-sec X --flat-folders --discard-chunks

1/first path is the main dir
2/second is where you want your files to be
3/ X is the number of seconds you need
4/flat folders parameter makes the tool take the files and export all of them as a big bulk into one folder. keeping this value empty will take the tracks and chunk them into specific folders with the track names. 
5/discard chunks will discard all the files that are smaller than the specified X

Useful tool! 
