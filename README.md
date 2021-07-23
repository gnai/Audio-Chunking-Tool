# Audio Chunking Tool
An audio tool using pydubs library with python to chunk your audio content into your desired length, with more flags to add. 

Example:

`python3 mp3_chunk.py --path <dirofaudiofiles> --boc-path <dirofchunks> --chunk-length-sec <int> --flat-folders --discard-chunks`

`--path` flag points out the directory where your audio files are, if they are structured in a way or another in subdirectories the script will keep the same structure of subdirs with the chunks of each track name in it. 

`--boc-path` target destination of chunks.

`--chunk-length-sec` an integer representing the desired chunk length in seconds.

`--flat folders` setting this value in the flags would dump all the chunks in one folder without the need to restructure the target dir as it is coming from the source dir, if not needed leave blank.

Example:

`python3 mp3_chunk.py --path <dirofaudiofiles> --boc-path <dirofchunks> --chunk-length-sec <int> --discard-chunks`

`--discard-chunks` fkag will discard all the files that are smaller than the specified chunk length, if not needed leave blank.

Example:

`python3 mp3_chunk.py --path <dirofaudiofiles> --boc-path <dirofchunks> --chunk-length-sec <int>`
