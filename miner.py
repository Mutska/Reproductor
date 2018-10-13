
from mp3_tagger import MP3File,VERSION_1,VERSION_2,VERSION_BOTH
mp3 = MP3File('test9.mp3')


tags = mp3.get_tags()
print(tags)
mp3.save()
