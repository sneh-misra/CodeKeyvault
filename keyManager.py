#!/usr/bin/python

import base64,json,os,sys, getopt,ConfigParser
from Crypto import Random
from Crypto.Cipher import AES
from ConfigParser import SafeConfigParser

GlobalConfigFile='config.ini'
GlobalConfigFileSection='mainSection'
Config = ConfigParser.ConfigParser()
Config.read(GlobalConfigFile)
GlobalSaltKeyTag=Config.get(GlobalConfigFileSection,'saltkeytag')
GlobalSaltKeyValue=Config.get(GlobalConfigFileSection,'saltkeyvalue')
GlobalKeyVaultFile=Config.get(GlobalConfigFileSection,'keyvaultfile')
GlobalKeyVaultFileSection=Config.get(GlobalConfigFileSection,'keyvaultsection')


def createSaltKey(operation,newPassword,newPasswordTag):
    """ To create a encrypted salt and save it as saltkey """
    
    newPasswordEncrypted=encrypt(GlobalSaltKeyValue,newPassword)
    
    if os.path.isfile(GlobalKeyVaultFile):
        if checkTag(GlobalKeyVaultFileSection,newPasswordTag):
            if operation == 'update':
                addUpdateTag(newPasswordTag, newPasswordEncrypted)
                print "Success-Password updated"
            else:
                print "Error:0001-Section and password tag already exists."
                sys.exit(2)

        else:
            if operation == 'add':    
                addUpdateTag(newPasswordTag, newPasswordEncrypted)
                print "Success-Password added"
            else:
                print "Error:0002-No matching tag found."
                sys.exit(2)
    else:
        print "Error:0003-Missing file ", GlobalKeyVaultFile
        sys.exit(2)

def checkSetUp():
    try:
        if os.path.isfile(GlobalKeyVaultFile):
            if GlobalSaltKeyValue:
               return True
    except:
        print "Error:0004-Please run setup to generate Salt Key"
        sys.exit(2)

def checkTag(section,tag):
    try:
        cfp = open(GlobalKeyVaultFile, 'r')
        ConfigTmp = ConfigParser.ConfigParser()
        ConfigTmp.read(GlobalKeyVaultFile)
        tagValue=ConfigTmp.get(section,tag)
        cfp.close()
        if tagValue:
            return True
        else:
            return False
    except:
        #print "Error:0004-Exception encountered while reading",GlobalKeyVaultFile
        return False

def getTagValue(fileName,section,tag):
    #try:
    print fileName
    print section
    print tag
    cfp = open(fileName, 'r')
    ConfigTmp = ConfigParser.ConfigParser()
    ConfigTmp.read(fileName)
    tagValue=ConfigTmp.get(section,tag)
    cfp.close()
    if tagValue:
        return tagValue
    else:
        print "No Tag found in",fileName
        sys.exit(2)
    #except:
    #    print "Error:0005-Exception encountered while reading",fileName
    #    sys.exit(2)

def addUpdateTag(newPasswordTag, newPasswordEncrypted):
    parser = SafeConfigParser()
    parser.read(GlobalKeyVaultFile)
    parser.set(GlobalKeyVaultFileSection,newPasswordTag, newPasswordEncrypted)
    with open(GlobalKeyVaultFile, 'wb') as configfile:
        parser.write(configfile)


def encrypt(key,msg ):
    base = 16
    pad = lambda s: s + (base - len(s) % base) * chr(base - len(s) % base)
    msg = pad(msg)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )
    return base64.b64encode( iv + cipher.encrypt(msg) )

def decrypt( key,enc ):
    unpad = lambda s : s[0:-ord(s[-1])]
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))


def main(argv):
    try:
        checkSetUp()
        action=''
        newPasswordTag=''
        newPassword=''
        operation=''
        passwordTag=''
        if len(sys.argv) < 3:
            print 'Usage1: keyManager.py -a <[encrypt|decrypt]> -o <[add|update]> -t <newPasswordTag> -k <newPassword>'
            sys.exit(2)
        opts, args = getopt.getopt(argv,'h:a:o:t:k:l', ['action=','operation=','newPasswordTag=','newPassword=', 'passwordTag=','help'])
    except getopt.GetoptError:
        print 'Usage2: keyManager.py -a <[encrypt|decrypt]> -o <[add|update]> -t <newPasswordTag> -k <newPassword>' 
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage3: keyManager.py -a <[encrypt|decrypt]> -o <[add|update]> -t <newPasswordTag> -k <newPassword>'
            sys.exit()
        elif opt in ("-a", "--action"):
            action = arg
            if action not in ['encrypt','decrypt']:
                print "Wrong -a argument, -a <[encrypt|decrypt]>"
                sys.exit(2)
        elif opt in ("-o", "--operation"):
            operation= arg 
        elif opt in ("-t", "--newPasswordTag"):
            newPasswordTag = arg
        elif opt in ("-k", "--newPassword"):
            newPassword = arg
        elif opt in ("-l", "--passwordTag"):
            passwordTag = arg
    if action == 'encrypt':
        if operation not in ['add','update']:
            print "Wrong -o argument, -o <[add|update]>"
            sys.exit(2)
        else:
            createSaltKey(operation,newPassword,newPasswordTag)
    elif action == 'decrypt':
        encryptedPassword= getTagValue(GlobalKeyVaultFile,GlobalKeyVaultFileSection,passwordTag)
        if encryptedPassword:
            print decrypt(GlobalSaltKeyValue,encryptedPassword)
        else:
            print "Error : Issue in fetching encrypted password from keyvault file"
            sys.exit(2)
    else:
        print 'Usage2: keyManager.py -a <[encrypt|decrypt]> -o <[add|update]> -t <newPasswordTag> -k <newPassword>'
        sys.exit(2)
        
    
if __name__ == '__main__':
    main(sys.argv[1:])
