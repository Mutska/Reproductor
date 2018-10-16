import os
from mp3_tagger import MP3File,VERSION_2


class miner(object):

    def __init__(self,dir):
        self.dir = dir
        self.mp3_files = []
        self.mp3_files_path = []
        self.mp3_tags = []



    def find_mp3_files(self):
        dir = os.getcwd()
        for file in os.listdir(dir):
            if file.endswith(".mp3"):
                self.mp3_files.append(file)
                f = open(file)
                self.mp3_files_path.append(os.path.abspath(f.name))
                f.close()

    def get_mp3_tags(self):
        for file in self.mp3_files:
            mp3 = MP3File(file)
            mp3.set_version(VERSION_2)
            self.mp3_tags.append(mp3)
        return self.mp3_tags




    #tags = mp3.get_tags()
    #print(tags)



