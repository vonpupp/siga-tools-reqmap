# -*- coding: utf-8 -*-
#!/usr/bin/env python

#   Project:			SIGA
#   Component Name:		reqmap
#   Language:			Python
#
#   License: 			GNU Public License
#       This file is part of the SIGA project specification stage.
#	This is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#       without even the implied warranty of MERCHANTABILITY or
#       FITNESS FOR A PARTICULAR PURPOSE.
#       See the GNU General Public License for more details.
#       <http://www.gnu.org/licenses/>
#
#   Author:			Albert De La Fuente (www.albertdelafuente.com)
#   E-Mail:			http://www.google.com/recaptcha/mailhide/d?k=01eb_9W_IYJ4Pm_Y9ALRIPug==&c=L15IEH_kstH8WRWfqnRyeW4IDQuZPzNDRB0KCzMTbHQ=
#
#   Description:		This script will map requirements/areas in a matrix
#        and build a csv representing the wireframes from the project
#
#   Limitations:		Time
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:		

"""
    Creates a CSV matrix with the mapping of requirements and areas.

    Command Line Usage:
        reqmap {<option> <argument>}

    Options:
        
    Examples:
        reqmap.py
"""

import getopt
import logging
import sys
import os
import csv
import codecs

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

class reqmap():
    """ Main problem class
    Attributes:
        - path, prependpath, replacepath, outfile: string
    """
    
    def __init__(self):
        # TODO: Private / protected
        self.__verbosity = VERB_NON
        self.__logger = logging.getLogger('reqmap')
        self.__loghdlr = None
        self.__formatter = None
        self.__mist = []
        self.__count = 0
        self.csvhdlr = None
        self.matrix=[[]]
        # Public
        self.path = ""
        self.prependpath = ""
        self.replacepath = ""
        self.outfile = "" # sys.stdout
        pass
    
    #---- internal support stuff
    
    def setVerbosity(self, v):
        self.__verbosity = v

    def logv(self, v, str):
        #print "logv().v=%d" % v
        #print "main().__verbosity=%d" % self.__verbosity
        if self.__verbosity >= v:
            print str

    def init(self, tag):
        self.matrix = []
        #values = [tag]
        #for i in range(1, self.maxtag+1):
        #    values = values + [tag + str(i).zfill(3)]
        #self.matrix.append(values)
        values = []
        self.matrix.append([tag])
        for i in range(1, self.maxtag+1):
            #values.append([tag + str(i).zfill(3)])
            self.matrix.append([tag + str(i).zfill(3)])
        #self.matrix.append(values)

        pass
        
    def loadFile(self, area, fullfilename):
        row = []
        lines = [area]
        f = open(fullfilename)
        for line in f.readlines():
            lines = lines + [line.rstrip('\n')]
        #row.append(lines)
        return lines
        pass
    
    def valueExists(self, v, column):
        i = 0
        exists = 0
        while i < len(column) and not exists:
            exists = column[i] == v
            i += 1
        return exists
    
    def printMatrix(self):
        for i, row in enumerate(self.matrix):
            print(self.matrix[i])

    
    def addColumn(self, tag, area, column):
        #row = []
        
        l = len(self.matrix)
        newcolumn = [area]
        #newcolumn.append([area])
        for i in range(1, self.maxtag+1):
            value = self.valueExists(tag + str(i).zfill(3), column)
            if value:
                newcolumn.append("1")
            else:
                newcolumn.append("")
                #newcolumn.append("0")

            #value = "0"
            #if self.valueExists(tag + str(i).zfill(3), column):
            #    newcolumn.append("1")
            #else:
            #    newcolumn.append("0")
            
        #for i, row in enumerate(self.matrix):
        for i, row in enumerate(self.matrix):
            print row
            row.append(newcolumn[i])
            #if tag + str(i).zfill(3) = :
         
        self.printMatrix()
        #self.matrix.append(values)
        #c4data = [header3, r1c3data, r2c3data]
        #for i, row in enumerate(matrix):
        #    row.append("0")
        #
        #for i in values:
        #    matrix[]
        pass
        
    def parseFilesPerTag(self, tag):
        self.logv(VERB_MED, "-> parse")
        self.__mist = []
        self.__count = 0
        #if self.path == ""
        for dirname, dirnames, filenames in os.walk(self.path):
            if '.svn' in dirnames:
                dirnames.remove('.svn')
            for subdirname in dirnames:
                pass
            for filename in filenames:
                if filename.endswith(('.list')) and tag in filename:
                    self.__count += 1
                    fullfilename = os.path.join(dirname, filename)
                    self.logv(VERB_MIN, "parsedir() => Parsing... %s" % (fullfilename))
                    values = self.loadFile(filename.split('.')[0], fullfilename)
                    self.addColumn(tag, filename.split('.')[0], values)
                    
                    #wffile = self.fixpath(wffile, self.replacepath, self.prependpath)

                    #wftuple = [filename, 'Artifact',
                        #'<a href="' + wffile + '"><font color="#0000ff"><u>' + wffile + '</u></font></a>',
                        #'File', 'Albert De La Fuente', filename, wffile]

                    #self.logv(2, "parsedir().wftuple=" + str(wftuple))
                    #self.logv(2, "parsedir().wftuple=%s" .join(map(str, wftuple)))
                    #self.__mist.append(wftuple)
                    pass
        self.logv(VERB_MIN, "parse...result=%d" % self.__count)
        self.logv(VERB_MED, "<- parse")
        return self.__count
    
    def totalize(self):
        colcount = []
        for j, row in enumerate(self.matrix[0]):
            colcount.append(0)
        
        for i in range(1, self.maxtag+1):
            for j, row in enumerate(self.matrix):
                if j >= 1:
                    colcount[int(j)] += int(self.matrix[i,int(j)])
                
        #for i, row in enumerate(self.matrix):
        #    print row
        #    row.append(newcolumn[i])
        pass

    
    def writecsv(self):
        if self.outfile != "":
            fh = open(self.outfile, 'wb')
            #fh = codecs.open(self.outfile, "wb", "utf-8")

            #fh = codecs.open(self.outfile, 'wb', encoding="utf-8")
        else:
            fh = sys.stdout

        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        #csvhdlr.writerow(["Name", "Type", "Notes", "Stereotype", "Author", "Alias", "GenFile"])
        for row in self.matrix:
            csvhdlr.writerow(row)

    def parseTag(self, maxtag, tag):
        self.maxtag = maxtag
        self.init(tag)
        self.outfile = self.path + tag + ".csv"
        
        self.logv(VERB_MIN, "outfile=%s" % self.outfile)
        self.parseFilesPerTag(tag)
        #m.logv(VERB_NON, "main.optarg = " .join(map(str, optarg)))
        #m.logv(1, "main.m.optarg = " .join(map(str, m.__mist)))
        #self.totalize()
        self.writecsv()
        print "INPUT:   " + self.path
        print "OUTPUT:  " + self.outfile
        #print " * Replace:  " + self.replacepath
        #print " * Fix with: " + self.prependpath
    
    #---- mainline

def main(argv):
    m = reqmap()
#    try:
#        optlist, args = getopt.getopt(argv[1:], 'hp:r:f:o:v:l:', ['help', 'path', 'replace', 'fix', 'out', 'verbose', 'log'])
#    except getopt.GetoptError, msg:
#        sys.stderr.write("wf2ea: error: %s" % msg)
#        sys.stderr.write("See 'wf2ea --help'.\n")
#        return 1
#
#    print str(optlist)
#    for opt, optarg in optlist:
#        if opt in ('-h', '--help'):
#            sys.stdout.write(__doc__)
#            return 0
#        elif opt in ('-p', '--path'):
#            m.path = optarg
#            pass
#        elif opt in ('-r', '--replace'):
#            m.replacepath = optarg # "/home/afu/siga/siga-svn/"
#            pass
#        elif opt in ('-f', '--fix'):
#            m.prependpath = optarg # "C:\\SIGA\\"
#            pass
#        elif opt in ('-o', '--out'):
#            m.outfile = optarg
#            m.logv(VERB_MED, "(-o) OUTPUT: %s" % optarg)
#            pass
#        elif opt in ('-v', '--verbose'):
#            #hdlr = logging.FileHandler('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')
#            #__formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#            #hdlr.setFormatter(__formatter)
#            #__logger.addHandler(hdlr)
#            m.setVerbosity(int(optarg))
#            #m.__verbosity = int(optarg)
##            print "(-v): " + str(m.__verbosity)
#            m.logv(VERB_MED, "main.optarg[%d]" % len(optlist))
#            m.logv(VERB_MED, "main.optarg = " .join(map(str, optarg)))
#            m.logv(VERB_MED, "main.optlist = " .join(map(str, optlist)))
#            #print "__verbosity=%d" % __verbosity
#            #m.__verbosity = int(optarg)
#            #print "__verbosity=%d" % __verbosity
#            #print "optarg=%s" % optarg
#            #if __verbosity == 2:
#            #    __logger.setLevel(logging.INFO)
#            #    __logger.info("Starting to log (INFO)...")
#            #elif __verbosity == 3:
#            #    __logger.setLevel(logging.DEBUG)
#            #    __logger.info("Starting to log (DEBUG)...")
#            pass
#        elif opt in ('-l', '--log'):
#            m.logfile = optarg            
#            m.logv(VERB_MED, "main.optarg = " .join(map(str, optarg)))
#            if m.isVerbose:
#                #m.logv(2, "main.optarg = " + optarg)
#                m.setLogger('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')
#            pass

    m.path = "/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-doc-reqareamap-csv/sources/lists/"
    m.setVerbosity(VERB_MED)

    m.parseTag(400, "RFI")
    m.parseTag(400, "RFN")
    m.parseTag(5, "RNF")
    m.parseTag(5, "RN")
    
    #m.writecsv()
    
    
#    print "m.verbosity=" + str(m.__verbosity)

    #if len(args) == 0:
    #    sys.stderr.write("wf2ea: error: incorrect number of "\
    #                     "arguments: argv=%r\n" % argv)
    #    return 1
    #else:
#    elif len(args) <= 1:
        #path = args[0]
        #if len(args) <= 2:
        #    outfile = argv[1]

    #try:
        #m.processDir(path) #, outfile) #, defines)
        #print "path=" + path
        #m.parseTag(path)
        #m.logv(2, "main.m.optarg = " .join(map(str, m.__mist)))
        #m.fixpaths()
        #m.writecsv()
        
        #m.processWF(path)
        #m.writecsv()
    #except: # PreprocessError, ex:
    #    sys.stderr.write("wf2ea: error: %s\n") # % str(ex))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
