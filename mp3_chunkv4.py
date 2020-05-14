import argparse
import os
import glob
import pprint
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import make_chunks

# label store will store metadata about songs
lbl_store = dict()

# location where to save the chunked files
boc_path = None

# Chunk length in seconds
chunk_length_sec = None

# create boc/label/track hierarchy
flat_folders = False

# Discard chunks that are not exactly at length of chunk-length-sec
discard_chunks = False

def print_lbl_store_info():
    # for now print the total number of labels
    print("Total {} labels".format(len(lbl_store)))

    # also print minimum number of songs in all labels
    min_songs_in_label = None
    for label in lbl_store.values():
        if min_songs_in_label is None  or len(label) < min_songs_in_label:
            min_songs_in_label = len(label)
    print("Minimum songs in label: {}".format(min_songs_in_label))

def extract_song_info(path):
    # song name is the file name without  the suffix
    song_name = os.path.basename(path).replace(".mp3", "")
    song_label = "UNKNOWN"
    path_elements = str(path).split("/")
    # song label is the second component of the path
    # the first one is the collection of labels driectory
    # files in the collection directory are categorized under
    # UNKNOWN label
    if len(path_elements) >= 3:
        song_label = path_elements[1]

    # return name and label
    return (song_name, song_label)

def chunk_song(song_path):
    # first extract song name and label it belongs to
    song_name, song_label = extract_song_info(song_path)

    if song_label not in lbl_store:
        lbl_store[song_label] = {}

    # if we have a duplicate song ignore it
    if song_name in lbl_store[song_label]:
        print("Duplicate song name {} in label {}".format(song_name, song_label))
        return


    # extract 60 second chunks of audio files and store them
    # in boc directory under <label>/<song name>/chunk<idx>
    if flat_folders:
        chunks_path = boc_path
    else:
        chunks_path = os.path.join(boc_path, song_label, song_name)
    print("Chunking {}".format(chunks_path))
    try:
        chunk_len = chunk_length_sec * 1000
        seg = AudioSegment.from_file(song_path , 'mp3')
        chunks = make_chunks(seg, chunk_len)
        os.makedirs(chunks_path, exist_ok=True)
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(chunks_path, "{}-c{}.mp3".format(song_name, i))
            if len(chunk) != chunk_len and discard_chunks:
                print("Discarding {} len {} < {} sec".format(chunk_path,
                                                             len(chunk) // 1000,
                                                             chunk_length_sec))
                continue
            print("Exporting {}".format(chunk_path))
            chunk.export(chunk_path, format='mp3')
    except:
        print("Chunking {} failed".format(chunks_path))
        return

    # store song path in label store for future statistics collection
    lbl_store[song_label][song_name] = song_path


def chunk_labels(labels_dir):
    # for each nested mp3 file song try to chunk it
    for path in Path(labels_dir).glob('**/*.mp3'):
        chunk_song(path)

def main():
    # boc_path will store the path of directory where we will
    # create all the label chunks
    global boc_path
    global chunk_length_sec
    global flat_folders
    global discard_chunks

    # simple command line argments to support running the program
    # with different labels path and different location of boc
    parser = argparse.ArgumentParser(description='Parse label songs into chunks')
    parser.add_argument('--path', required=True, dest='path',
                        help='labels dir path')
    parser.add_argument('--boc-path', required=True, dest='boc_path',
                        help='Bag of chunks path')
    parser.add_argument('--chunk-length-sec', required=False, default=60,
                        dest='chunk_length_sec', type=int,
                        help='Length of each chunk in seconds')
    parser.add_argument('--flat-folders', action='store_true', default=False,
                        dest='flat_folders',
                        help='Do not create label/track folder hierarchy')
    parser.add_argument('--discard-chunks', action='store_true', default=False,
                        dest='discard_chunks',
                        help='Discard chunks that are not exactly at length of chunk-length-sec')
    args = parser.parse_args()
    boc_path = args.boc_path
    chunk_length_sec = args.chunk_length_sec
    flat_folders = args.flat_folders
    discard_chunks = args.discard_chunks

    # chunk labels
    chunk_labels(args.path)
    # print statistics on processed labels
    print_lbl_store_info()

if __name__ == '__main__':
    main()
