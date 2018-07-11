#!/usr/bin/python
## Initial setup


import os,sys,getopt
from ConfigParser import SafeConfigParser

def checkSetUp(configFile,sectionName,saltKeyTag,saltKeyValue,keyVaultFileName,keyVaultSection):
    #try:
    if os.path.isfile(configFile):
        print "Error:0001-",configFile," already exists, remove it and run keyManagerSetUp.py do a fresh setup"
        sys.exit(2)
    else:            
        addSection(configFile,sectionName)
        addUpdateTag(configFile, sectionName, 'saltKeyTag', saltKeyTag)
        addUpdateTag(configFile, sectionName, 'saltKeyValue', saltKeyValue)
        addUpdateTag(configFile, sectionName, 'keyVaultFile', keyVaultFileName)
        addUpdateTag(configFile, sectionName, 'keyVaultSection', keyVaultSection)
        addSection(keyVaultFileName,keyVaultSection)

    #except:
    #    print "Error:0004-Please fix the error and re-run"
    #    sys.exit(2)

def addSection(configFile,sectionName):
    try:
        Config = SafeConfigParser()
        cfgfile = open(configFile,'w+')
        Config.add_section(sectionName)
        Config.write(cfgfile)
        cfgfile.close()
    except:
        print "Error:0005-Somthing went wrong while creating section"
        sys.exit(2)

def addUpdateTag(configFile, sectionName, tag, value):
    parser = SafeConfigParser()
    parser.read(configFile)
    parser.set(sectionName, tag, value)
    with open(configFile, 'wb') as configfile:
        parser.write(configfile)


def main(argv):
    try:
        configFile = 'config.ini'
        sectionName = 'mainSection'
        saltKeyTag=''
        saltKeyValue=''
        keyVaultFileName=''
        keyVaultDefaultSection='keyVaultSection'

        if len(sys.argv) < 3:
            print 'Usage: keyManagerSetUp.py -t <saltKeyTag> -k <saltKeyValue> -f <keyVaultFileName>'
            sys.exit(2)
        opts, args = getopt.getopt(argv,'h:t:k:f:s', ['saltKeyTag=','saltKeyValue=','keyVaultFileName=','help'])
    except getopt.GetoptError:
        print 'Usage: keyManagerSetUp.py -t <saltKeyTag> -k <saltKeyValue> -f <keyVaultFileName>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: keyManagerSetUp.py -t <saltKeyTag> -k <saltKeyValue> -f <keyVaultFileName>'
            sys.exit()
        elif opt in ("-t", "--saltKeyTag"):
            saltKeyTag = arg
        elif opt in ("-k", "--saltKeyValue"):
            saltKeyValue = arg
            if len(saltKeyValue) not in [16,24,32]:
                print "Error:0002-saltKeyValue must be either 16, 24, or 32 bytes long, else app will not work"
                sys.exit(2)
        elif opt in ("-f", "--keyVaultFileName"):
            keyVaultFileName = arg
    checkSetUp(configFile,sectionName,saltKeyTag,saltKeyValue,keyVaultFileName,keyVaultDefaultSection)





if __name__ == '__main__':
    main(sys.argv[1:])

