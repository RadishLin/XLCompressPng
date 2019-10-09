#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys
import time
import subprocess,shlex

totalSave = 0

def executeShellCommand(COMMAND):
    subprocess.call(shlex.split(COMMAND))

def searchPngCompress(rootpath):
    for path in os.listdir(rootpath):
        fullpath = os.path.join(rootpath, path)
        if os.path.isdir(fullpath):
            searchPngCompress(fullpath)
        elif os.path.isfile(fullpath):
            if fullpath.lower().endswith('.png'):
                executeShellCommand('./pngquant --ext .png.tmp "%s"' % (fullpath))
                tmpPath = fullpath + '.tmp'
                if os.path.isfile(tmpPath):
                    originalSize = os.path.getsize(fullpath)
                    newSize = os.path.getsize(tmpPath)
                    global totalSave
                    totalSave = totalSave + (originalSize - newSize)
                    print('\033[0;32m%s Successfully Compressed %dKB %.0f%%\033[0m' % (fullpath, (originalSize - newSize) / 1024, (1 - newSize / originalSize) * 100.0))
                    executeShellCommand('rm "%s"' % fullpath)
                    os.rename(tmpPath, fullpath)


if len(sys.argv) >= 2:
    rootPath = sys.argv[1]
    startTime = time.time()
    searchPngCompress(rootPath)
    print('\033[0;32mCompression End. Total Save: %dKB. Cost: %.2fs\033[0m' % (totalSave / 1024, time.time() - startTime))
else:
    print('\033[0;31mError - Because need a project root path \033[0m')



