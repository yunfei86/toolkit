#!/usr/bin/env python
import sys, os, argparse
from re         import search
from logbase    import LogBase

class ReadVCOut(object):
    somaticLineHeader = {'smSnpSensitivityMajor':'Somatic SNP Sensitivity Major',
                         'smSnpSensitivityMinor':'Somatic SNP Sensitivity Minor',
                         'smIndelsSensitivityMajor':'Somatic Indels Sensitivity Major',
                         'smIndelsSensitivityMinor':'Somatic Indels Sensitivity Minor',
                         'smOverallSensitivityMajor':'Somatic Overall Sensitivity Major',
                         'smOverallSensitivityMinor':'Somatic Overall Sensitivity Minor',
                         'smSnpFalseDiscoveryRate':'Somatic SNP False DiscoveryRate',
                         'smIndelsFalseDiscoveryRate':'Somatic Indels False Discovery Rate',
                         'smOverallFalseDiscoveryRate':'Somatic Overall False Discovery Rate'}
    germLineHeader =   {'glSnpSensitivity':'Germline SNP Sensitivity',
                        'glIndelsSensitivity':'Germline Indels Sensitivity',
                        'glOverallSensitivity':'Germline Overall Sensitivity',
                        'glSnpFalseDiscoveryRate':'Germline SNP False Discovery Rate',
                        'glIndelsFalseDiscoveryRate':'Germline Indels False Discovery Rate',
                        'glOverallFalseDiscoveryRate':'Germline Overall False Discovery Rate',}
    somaticList = ['smSnpSensitivityMajor', 'smSnpSensitivityMinor',
                   'smIndelsSensitivityMajor', 'smIndelsSensitivityMinor',
                   'smOverallSensitivityMajor', 'smOverallSensitivityMinor',
                   'smSnpFalseDiscoveryRate', 'smIndelsFalseDiscoveryRate', 'smOverallFalseDiscoveryRate']
    germlineList = ['glSnpSensitivity', 'glIndelsSensitivity',
                    'glOverallSensitivity', 'glSnpFalseDiscoveryRate', 'glIndelsFalseDiscoveryRate',
                    'glOverallFalseDiscoveryRate']
    somaticOutput = {'smSnpSensitivityMajor':None, 'smSnpSensitivityMinor':None,
                     'smIndelsSensitivityMajor':None, 'smIndelsSensitivityMinor':None,
                     'smOverallSensitivityMajor':None, 'smOverallSensitivityMinor':None,
                     'smSnpFalseDiscoveryRate':None, 'smIndelsFalseDiscoveryRate':None,
                     'smOverallFalseDiscoveryRate':None}
    germlineOutput = {'glSnpSensitivity':None, 'glIndelsSensitivity':None, 'glOverallSensitivity':None,
                      'glSnpFalseDiscoveryRate':None, 'glIndelsFalseDiscoveryRate':None,
                      'glOverallFalseDiscoveryRate':None}

    def __init__(self, fileName=None, debugLevel='info'):
        logBase = LogBase('ReadVCOut',debugLevel)
        logBase.createRotatingFileLogger('log/ionunittest.log')
        self.logger = logBase.logger        
        if fileName:
            self.fileName = fileName
            
    def setFileName(self, fileName):
        if fileName:
            self.fileName = fileName
        else:
            self.logger.warn('Input file name can not be None!')
            raise Exception('Input file name can not be None!')
        
    def getFileName(self):
        return self.fileName
        
    def readFile(self, fileName=None):
        try:
            if fileName:
                self.fileName = fileName
            inFile = open(self.fileName, 'r')
            self.data = {}
            for line in inFile:
                if search(":", line):
                    cleanLine = str.strip(line)
                    cleanLineList = cleanLine.split(":")
                    if len(cleanLineList) != 2:
                        self.logger.warn('Line [%s] is not having one colon[:]!'%cleanLine)
                    else:
                        self.data[str.strip(cleanLineList[0]).lower()] = str.strip(cleanLineList[1])
        except:
            self.logger.exception(sys.exc_info)
            
    def glSnpSensitivity(self):
        #SNP Senitivity = (Total Number of TP SNPs in Major) / (Total Number of SNPs in Major Truth File)
        numeratorStr = 'Total Number of TP SNPs in Major'
        denominatorStr = 'Total Number of SNPs in Major Truth File'
        numerator = float(self.data[numeratorStr.lower()])
        denominator = float(self.data[denominatorStr.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(denominatorStr, denominator))
        if denominator == 0:
            return 'Infinity'        
        retValue = numerator / denominator
        self.logger.debug('%s = %s / %s'%(retValue, numerator, denominator))
        return retValue
        
    def glIndelsSensitivity(self):
        #InDel Sensitivity = (Total Number of TP Indels in Major) / (Total Number of Deletion in Major Truth File + Total Number of Insertions in Major Truth File)

        numeratorStr = 'Total Number of TP Indels in Major'
        numerator = float(self.data[numeratorStr.lower()])
        d1Str = 'Total Number of Deletion in Major Truth File'
        d2Str = 'Total Number of Insertions in Major Truth File'
        d1 = float(self.data[d1Str.lower()])
        d2 = float(self.data[d2Str.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('d1:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('d2:')
        self.logger.debug('%s: %s'%(d2Str, d2))
        denominator = d1 + d2
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = %s / (%s + %s)'%(retValue, numerator, d1, d2))
        return retValue

    def glOverallSensitivity(self):
        #Overall Sensitivity = (Total Number of TP SNPs in Major + Total Number of TP Indels in Major) / (Total Number of Variants in Major Truth file)

        n1Str = 'Total Number of TP SNPs in Major'
        n2Str = 'Total Number of TP Indels in Major'
        n1 = float(self.data[n1Str.lower()])
        n2 = float(self.data[n2Str.lower()])
        numerator = n1 + n2
        denominatorStr = 'Total Number of Variants in Major Truth file'
        denominator = float(self.data[denominatorStr.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(n1Str, n1))
        self.logger.debug('%s: %s'%(n2Str, n2))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(denominatorStr, denominator))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = (%s + %s) / %s'%(retValue, n1, n2, denominator))
        return retValue
        
    def glSnpFalseDiscoveryRate(self):
        #SNP False Discovery Rate = (Total Number of FP SNPs) / (Total Number of TP SNPs in Major + Total Number of FP SNPs)
        
        numeratorStr = 'Total Number of FP SNPs'
        d1Str = 'Total Number of TP SNPs in Major'
        numerator = float(self.data[numeratorStr.lower()])
        d1 = float(self.data[d1Str.lower()])
        denominator = d1 + numerator
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = %s / (%s + %s)'%(retValue, numerator, d1, numerator))
        return retValue
        
    def glIndelsFalseDiscoveryRate(self):
        #InDel False Discovery Rate = (Total Number of FP Indels)  / (Total Number of TP Indels in Major + Total Number of FP Indels)

        numeratorStr = 'Total Number of FP Indels'
        d1Str = 'Total Number of TP Indels in Major'
        numerator = float(self.data[numeratorStr.lower()])
        d1 = float(self.data[d1Str.lower()])
        denominator = d1 + numerator
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = %s / (%s + %s)'%(retValue, numerator, d1, numerator))
        return retValue
        
    def glOverallFalseDiscoveryRate(self):
        #Overall False Discovery Rate =  (Total Number of FP SNPs + Total Number of FP Indels) /
        #(Total Number of FP SNPs + Total Number of FP Indels + Total Number of TP SNPs in Major + Total Number of TP Indels in Major)

        n1Str = 'Total Number of FP SNPs'
        n2Str = 'Total Number of FP Indels'
        n1 = float(self.data[n1Str.lower()])
        n2 = float(self.data[n2Str.lower()])
        numerator = n1 + n2
        d1Str = 'Total Number of TP SNPs in Major'
        d2Str = 'Total Number of TP Indels in Major'
        d1 = float(self.data[d1Str.lower()])
        d2 = float(self.data[d2Str.lower()])
        denominator = d1 + d2 + n1 + n2
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(n1Str, n1))
        self.logger.debug('%s: %s'%(n2Str, n2))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('%s: %s'%(d2Str, d2))
        self.logger.debug('%s: %s'%(n1Str, n1))
        self.logger.debug('%s: %s'%(n2Str, n2))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = (%s + %s) / (%s + %s + %s + %s)'%(retValue, n1, n2, d1, d2, n1, n2))
        return retValue

    def smSnpSensitivityMajor(self):
        #SNP Senitivity Major Allele = (Total Number of TP SNPs in Major) / (Total Number of SNPs in Major Truth File)
        
        numeratorStr = 'Total Number of TP SNPs in Major'
        denominatorStr = 'Total Number of SNPs in Major Truth File'
        numerator = float(self.data[numeratorStr.lower()])
        denominator = float(self.data[denominatorStr.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(denominatorStr, denominator))
        if denominator == 0:
            return 'Infinity'        
        retValue = numerator / denominator
        self.logger.debug('%s = %s / %s'%(retValue, numerator, denominator))
        return retValue

    def smSnpSensitivityMinor(self):
        #SNP Senitivity Minor Allele = (Total Number of TP SNPs in Minor) / (Total Number of SNPs in Minor Truth File)
        
        numeratorStr = 'Total Number of TP SNPs in Minor'
        denominatorStr = 'Total Number of SNPs in Minor Truth File'
        numerator = float(self.data[numeratorStr.lower()])
        denominator = float(self.data[denominatorStr.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(denominatorStr, denominator))
        if denominator == 0:
            return 'Infinity'        
        retValue = numerator / denominator
        self.logger.debug('%s = %s / %s'%(retValue, numerator, denominator))
        return retValue

    def smIndelsSensitivityMajor(self):
        #InDel Sensitivity Major Allele = (Total Number of TP Indels in Major) /
        #(Total Number of Deletion in Major Truth File + Total Number of Insertions in Major Truth File)

        numeratorStr = 'Total Number of TP Indels in Major'
        numerator = float(self.data[numeratorStr.lower()])
        d1Str = 'Total Number of Deletion in Major Truth File'
        d2Str = 'Total Number of Insertions in Major Truth File'
        d1 = float(self.data[d1Str.lower()])
        d2 = float(self.data[d2Str.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('d1:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('d2:')
        self.logger.debug('%s: %s'%(d2Str, d2))
        denominator = d1 + d2
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = %s / (%s + %s)'%(retValue, numerator, d1, d2))
        return retValue
        
    def smIndelsSensitivityMinor(self):
        #InDel Sensitivity Minor Allele = (Total Number of TP Indels in Minor) /
        #(Total Number of Deletion in Minor Truth File + Total Number of Insertions in Minor Truth File)

        numeratorStr = 'Total Number of TP Indels in Minor'
        numerator = float(self.data[numeratorStr.lower()])
        d1Str = 'Total Number of Deletion in Minor Truth File'
        d2Str = 'Total Number of Insertions in Minor Truth File'
        d1 = float(self.data[d1Str.lower()])
        d2 = float(self.data[d2Str.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('d1:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('d2:')
        self.logger.debug('%s: %s'%(d2Str, d2))
        denominator = d1 + d2
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = %s / (%s + %s)'%(retValue, numerator, d1, d2))
        return retValue
        
    def smOverallSensitivityMajor(self):
        #Overall Sensitivity Major Allele = (Total Number of TP SNPs in Major + Total Number of TP Indels in Major) / (Total Number of Variants in Major Truth file)

        n1Str = 'Total Number of TP SNPs in Major'
        n2Str = 'Total Number of TP Indels in Major'
        n1 = float(self.data[n1Str.lower()])
        n2 = float(self.data[n2Str.lower()])
        numerator = n1 + n2
        denominatorStr = 'Total Number of Variants in Major Truth file'
        denominator = float(self.data[denominatorStr.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(n1Str, n1))
        self.logger.debug('%s: %s'%(n2Str, n2))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(denominatorStr, denominator))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = (%s + %s) / %s'%(retValue, n1, n2, denominator))
        return retValue
        
    def smOverallSensitivityMinor(self):
        #Overall Sensitivity Minor Allele = (Total Number of TP SNPs in Minor + Total Number of TP Indels in Minor) / (Total Number of Variants in Minor Truth file)

        n1Str = 'Total Number of TP SNPs in Minor'
        n2Str = 'Total Number of TP Indels in Minor'
        n1 = float(self.data[n1Str.lower()])
        n2 = float(self.data[n2Str.lower()])
        numerator = n1 + n2
        denominatorStr = 'Total Number of Variants in Minor Truth file'
        denominator = float(self.data[denominatorStr.lower()])
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(n1Str, n1))
        self.logger.debug('%s: %s'%(n2Str, n2))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(denominatorStr, denominator))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = (%s + %s) / %s'%(retValue, n1, n2, denominator))
        return retValue
    
        
    def smSnpFalseDiscoveryRate(self):
        #SNP False Discovery Rate = (Total Number of FP SNPs) /
        #(Total Number of TP SNPs in Minor + Total Number of TP SNPs in Major + Total Number of FP SNPs) *

        numeratorStr = 'Total Number of FP SNPs'
        numerator = float(self.data[numeratorStr.lower()])
        d1Str = 'Total Number of TP SNPs in Minor'
        d2Str = 'Total Number of TP SNPs in Major'
        d3Str = 'Total Number of FP SNPs'
        d1 = float(self.data[d1Str.lower()])
        d2 = float(self.data[d2Str.lower()])
        d3 = float(self.data[d3Str.lower()])
        denominator = d1 + d2 + d3
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('%s: %s'%(d2Str, d2))
        self.logger.debug('%s: %s'%(d3Str, d3))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = %s / (%s + %s + %s)'%(retValue, numerator, d1, d2, d3))
        return retValue
    
    def smIndelsFalseDiscoveryRate(self):
        #Indel False Discovery Rate = (Total Number of FP Indels) /
        #(Total Number of TP Indels in Minor + Total Number of TP Indels in Major + Total Number of FP Indels) *

        numeratorStr = 'Total Number of FP Indels'
        numerator = float(self.data[numeratorStr.lower()])
        d1Str = 'Total Number of TP Indels in Minor'
        d2Str = 'Total Number of TP Indels in Major'
        d3Str = 'Total Number of FP Indels'
        d1 = float(self.data[d1Str.lower()])
        d2 = float(self.data[d2Str.lower()])
        d3 = float(self.data[d3Str.lower()])
        denominator = d1 + d2 + d3
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(numeratorStr, numerator))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('%s: %s'%(d2Str, d2))
        self.logger.debug('%s: %s'%(d3Str, d3))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = %s / (%s + %s + %s)'%(retValue, numerator, d1, d2, d3))
        return retValue
        
    def smOverallFalseDiscoveryRate(self):
        #Overall False Discovery Rate =  (Total Number of FP SNPs + Total Number of FP Indels) /
        #(Total Number of FP SNPs + Total Number of FP Indels + Total Number of TP SNPs in Major +
        #Total Number of TP Indels in Major + Total Number of TP SNPs in Minor + Total Number of TP Indels in Minor) *

        n1Str = 'Total Number of FP SNPs'
        n2Str = 'Total Number of FP Indels'
        n1 = float(self.data[n1Str.lower()])
        n2 = float(self.data[n2Str.lower()])
        numerator = n1 + n2
        d1Str = 'Total Number of FP SNPs'
        d2Str = 'Total Number of FP Indels'
        d3Str = 'Total Number of TP SNPs in Major'
        d4Str = 'Total Number of TP Indels in Major'
        d5Str = 'Total Number of TP SNPs in Minor'
        d6Str = 'Total Number of TP Indels in Minor'
        d1 = float(self.data[d1Str.lower()])
        d2 = float(self.data[d2Str.lower()])
        d3 = float(self.data[d3Str.lower()])
        d4 = float(self.data[d4Str.lower()])
        d5 = float(self.data[d5Str.lower()])
        d6 = float(self.data[d6Str.lower()])
        
        denominator = d1 + d2 + d3 + d4 +d5 + d6
        self.logger.debug('Numerator:')
        self.logger.debug('%s: %s'%(n1Str, n1))
        self.logger.debug('%s: %s'%(n2Str, n2))
        self.logger.debug('Denominator:')
        self.logger.debug('%s: %s'%(d1Str, d1))
        self.logger.debug('%s: %s'%(d2Str, d2))
        self.logger.debug('%s: %s'%(d3Str, d3))
        self.logger.debug('%s: %s'%(d4Str, d4))
        self.logger.debug('%s: %s'%(d5Str, d5))
        self.logger.debug('%s: %s'%(d6Str, d6))
        if denominator == 0:
            return 'Infinity'
        retValue = numerator / denominator
        self.logger.debug('%s = (%s + %s) / (%s + %s + %s + %s+ %s + %s)'%(retValue, n1, n2, d1, d2, d3, d4, d5, d6))
        return retValue
        
    def computeGermline(self):
        for pName in self.germlineList:
            proc = getattr(self, pName)
            self.logger.debug(pName.center(80,'='))
            self.germlineOutput[pName] = proc()
            self.logger.debug('Done'.center(80,'-'))

    def computeSomatic(self):
        for pName in self.somaticList:
            proc = getattr(self, pName)
            self.logger.debug(pName.center(80,'='))
            self.somaticOutput[pName] = proc()
            self.logger.debug('Done'.center(80,'-'))

    def printgermline(self, svn, svnDate):
        self.readFile()
        self.computeGermline()
    
        print '%s, %s, %s, '%(self.getFileName(), svn, svnDate),
        for g in self.germlineList:
            print '%s, '%self.germlineOutput[g],
        print ''
        
    def printsomatic(self, svn, svnDate):
        self.readFile()
        self.computeSomatic()
        print '%s, %s, %s, '%(self.getFileName(), svn, svnDate),
        for s in self.somaticList:
            print '%s, '%self.somaticOutput[s],
        print ''
    
    def printgermlineHeader(self):
        print 'Input File, SVN, Date, ',
        for g in self.germlineList:
            print '%s, '%self.germLineHeader[g],
        print ''
    
    def printsomaticHeader(self):
        print 'Input File, SVN, Date, ',
        for s in self.somaticList:
            print '%s, '%self.somaticLineHeader[s],
        print ''    

def getSvn(fileName):
    fileNameList = fileName.split("_")
    return fileNameList[3]

def getDate(fileName):
    fileNameList = fileName.split("_")
    return '%s-%s-%s'%(fileNameList[-1][2:4], fileNameList[-1][4:6], fileNameList[-1][:2])

def main():
    parser = argparse.ArgumentParser(description='This script starts a series of tests.')
    parser.add_argument('-r', '--rootData', help='Mandatory. The location where all of the data are available.')
    parser.add_argument('-t', '--type', help='Optional. The type is "germline" or "somatic". Default: germline')
    parser.add_argument('-l', '--level', help='Optional. The level is "low" or "high". Default: low')
    parser.add_argument('-c', '--colHeader', help='Optional. Column header flag.True or False. Default: False', action='store_true', default=False)
    parser.add_argument('-d', '--debug', help='Optional. Debug flag.True or False. Default: False', action='store_true', default=False)
    args = parser.parse_args()

    if args.rootData == None:
        print 'Please specify the directory where the tests are located'
        parser.print_usage()
        sys.exit(1)

    if args.type == None:
        args.type = 'germline'

    if args.level == None:
        args.level = 'low'

    if args.debug:
        dLevel = 'debug'
    else: dLevel = 'info'
    
    svnTag = getSvn(args.rootData)
    svnDate = getDate(args.rootData)
    rvc = ReadVCOut(fileName=None, debugLevel = dLevel)
    fileName = 'vcout_%s_%s_summary_stats.txt'%(args.type, args.level)
    rvc.setFileName(os.path.join(args.rootData, fileName))
    if args.colHeader:
        getattr(rvc, 'print%sHeader'%args.type)()
    getattr(rvc, 'print%s'%args.type)(svnTag, svnDate)

if __name__ == '__main__':
    main()