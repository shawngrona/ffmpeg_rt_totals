
"""
FFMPEG Totals
"""
import sys
import os.path
import subprocess
import re 
from decimal import Decimal
topdir = ''
ffmpeg_path = ''
exten = ''
total_length = 0

def step(ext, dirname, names):
    global total_length
    ext = ext.lower()
    for name in names:
        if name.lower().endswith(ext):
            path=os.path.join(dirname, name)
            length = get_video_length(path)

           

def get_video_length(path):
  global total_length
  process = subprocess.Popen([ffmpeg_path, '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = process.communicate()
  matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL)

  total = 0
  if (matches != None):
    matches = matches.groupdict()
    hours = Decimal(matches['hours'])
    minutes = Decimal(matches['minutes'])
    seconds = Decimal(matches['seconds'])
   
    total += 60 * 60 * hours
    total += 60 * minutes
    total += seconds
    total = total / 60; # minutes
    total_length = total_length+total
  print(path+' duration = '+str(total))

cmdargs = str(sys.argv)
topdir = str(sys.argv[1])
ffmpeg_path = str(sys.argv[2])
exten = str(sys.argv[3])
os.path.walk(topdir, step, exten)
print('Total Duration = '+str(total_length)) 
