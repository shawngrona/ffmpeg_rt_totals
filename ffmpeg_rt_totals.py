#!/usr/bin/env python

#
# Copyright 2012 BloomReach, Inc.
# Portions Copyright 2014 Databricks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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
  matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

  total = 0
  if (matches != None):
    hours = Decimal(matches['hours'])
    minutes = Decimal(matches['minutes'])
    seconds = Decimal(matches['seconds'])
   
    total += 60 * 60 * hours
    total += 60 * minutes
    total += seconds
    total = total / 60; # minutes
    total_length = total_length+total
  print('Found File, duration = '+str(total))

cmdargs = str(sys.argv)
topdir = str(sys.argv[1])
ffmpeg_path = str(sys.argv[2])
exten = str(sys.argv[3])
os.path.walk(topdir, step, exten)
print('Total Duration = '+str(total_length)) 