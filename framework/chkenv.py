#!/usr/bin/env python
import sys, os, time, traceback

utilpath = os.path.join('src','utils')
if utilpath not in sys.path:
    sys.path.insert(0, utilpath)

from ionsystem import IonSystem
from logbase   import LogBase

iSystem = IonSystem()

def chkDir(dirName):
    if not os.path.exists(dirName):
        raise Exception('Directory [%s] does not exists!'%dirName)
    return True

def install(dirName, packageName):
    saveDir = os.getcwd()
    if (chkDir(dirName)):
        os.chdir(dirName)
        iSystem.execute('tar -xvzf %s'%packageName)
        if (iSystem.noError()):
            tmpList = packageName.split('.tar')
            if (len(tmpList) == 2):
                if (chkDir(tmpList[0])):
                    os.chdir(tmpList[0])
                    iSystem.execute('sudo python ./setup.py build')
                    if (iSystem.noError()):
                        iSystem.execute('sudo python ./setup.py install')
    os.chdir(saveDir)


logBase = LogBase('CheckEnv')

if (not os.path.exists('log')):
    os.mkdir('log')
    logBase.createFileLogger('log/chkenv.log', 'debug')

logger = logBase.logger

if (chkDir('src')):
    logger.info('Source directory [src] available...')
if (chkDir('requiredpackage')):
    logger.info('Source directory [requiredpackage] available...')
    
logger.info('Checking for Python Version...')

verNum = float(sys.version.split()[0][:-2])
if 2.4 <= verNum <= 2.6:
    try:
        from unittest2 import result
        logger.info('unittest2 is installed already!')
    except:
        logger.info('Attempting to install unittest2-0.5.1.tar.gz...')
        install('requiredpackage', 'unittest2-0.5.1.tar.gz')
            
    try:
        from ordereddict import OrderedDict
    except:
        logger.info('Attempting to install ordereddict-1.1.tar.gz...')
        install('requiredpackage', 'ordereddict-1.1.tar.gz')

iSystem.execute('which epydoc')
if (iSystem.noError()):
    if (len(iSystem.getStdOut()) == 0):
        logger.info('Attempting to install the document generation software...')
        iSystem.execute('sudo apt-get --quiet --assume-yes --force-yes install python-epydoc')

    logger.info('Attempting to generate Documentation for the Ion Test Framework...')

    iSystem.execute(os.path.join(os.getcwd(), 'mkdoc.sh'), shellFlag = True)
    if (chkDir('index.html')):
        logger.info('Documents generated successfully! Please load index.html in your favourite browser and you are good to start...')
