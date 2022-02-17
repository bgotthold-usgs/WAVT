import numpy as np
import soundfile as sf
import struct
import time
import datetime
  
filename = '20211025_030626T.WAV'

date_string = filename.replace('T.WAV','')
recording_time = datetime.datetime.strptime(date_string,"%Y%m%d_%H%M%S")
data, sr = sf.read(filename)

print(recording_time)

def read_in_chunks(file_object, chunk_size=512):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

pointer = 0
split = bytearray()
header =  bytearray()
with open(filename, 'rb') as f:
    chunk_size = 512
    for i, chunk in enumerate(read_in_chunks(f, chunk_size=chunk_size)):
        pointer = pointer + chunk_size
        if i == 0:
            
            int16 = struct.unpack("<i", chunk[4:8]) # little-endian
            int16 = struct.unpack("<i", chunk[484:488]) # little-endian
            header += bytearray(chunk)
            
        else:
            split += bytearray(chunk)
            empty = []
            for j in range(0, 64, 2):
                int16 = struct.unpack("<h", chunk[j:j+2])[0] # little-endian
                if int16 == 1:
                    empty.append(1)
                elif int16 == -1:
                    empty.append(0)
            empty.reverse()

            if len(empty) == 32:
                x = int(''.join(map(str,empty)), 2)
                if x > 0:
                    header[4:8] = (len(split) + 512 -8).to_bytes(4, 'little') 
                    
                    header[484:488] = (len(split) + 512 -488).to_bytes(4, 'little')                 
                   
                    newFile = open('xx_{}.WAV'.format(recording_time), "wb")
                    newFile.write(header)
                    newFile.write(split)
                    newFile.close()
                    pointer += (x * 512)
                    recording_time = recording_time + datetime.timedelta(seconds=pointer/(2 * sr))
                    split = bytearray()



 
