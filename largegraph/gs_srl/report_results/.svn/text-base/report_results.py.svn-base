'''
Created on Nov 13, 2015

@author: irma
'''
import argparse,os
import furer_report, false_furer_report, random_report,exhaustive_report,false_furer_report_orderings

if __name__=='__main__':
        parser = argparse.ArgumentParser(description='Run exhaustive approach')
        parser.add_argument('-r',help='file containing paths to all the selected patterns')
        parser.add_argument('-d',help='path to data graph')
        parser.add_argument('-redo',default=False,action='store_true',help='redo report')
        parser.add_argument('-appr',nargs='+',default=["furer","ffurer","random","exhaustive","ffurer_ord"],help='approaches to do')
        parser.add_argument('-write',default=False,action='store_true',help='redo report')

        args = parser.parse_args()
        approaches=args.appr
        patterns=[]
        stringAllInterruptedPatternsFurer=[]
        stringAllInterruptedPatternsRandom=[]
        stringAllInterruptedPatternsFurerAD=[]
        stringAllInterruptedPatternsExhaustive=[]
        with open(args.r,'r') as f:
            for line in f.readlines():
                patterns.append(line.rstrip())
        for appr in args.appr:
            if appr=="furer":
                for line in patterns:
                    print "reporting: ",line
                    if not os.path.exists(os.path.join(line,'complete.info')):
                        stringAllInterruptedPatternsFurer.append(line)
                    try:
                       furer_report.main(line, args.d, args.redo,args.write,None)
                    except:
                       print "COULDN'T REPORT THIS ONE! ERROR!"
                print "Furer finished!"
            if appr=="ffurer":
                for line in patterns:
                  if not os.path.exists(os.path.join(line,'complete.info')):
                        stringAllInterruptedPatternsFurerAD.append(line)
                  print "reporting: ",line
                  try:
                     false_furer_report.main(line, args.d, args.redo,args.write,None)
                  except:
                      print "Couldn't report this one!"
                print "False Furer finished!"
            
            if appr=="ffurer_ord":
                for line in patterns:
                  if not os.path.exists(os.path.join(line,'complete.info')):
                        stringAllInterruptedPatternsFurerAD.append(line)
                  print "reporting: ",line
                  try:
                     false_furer_report_orderings.main(line, args.d, args.redo,args.write,None)
                  except:
                      print "Couldn't report this one!"
                print "False Furer Ordered finished!"
            
            if appr=="random":
                for line in patterns:
                    if not os.path.exists(os.path.join(line,'complete.info')):
                        stringAllInterruptedPatternsRandom.append(line)
                    print "reporting: ",line
                    try:
                       random_report.main(line,args.d,args.redo,"my",args.write,None)
                    except:
                        print "Couldn't report this one!"
                print "Random vertex finished!"
            
            if appr=="exhaustive":
                for line in patterns: 
                  print "reporting: ",line
                  if not os.path.exists(os.path.join(line,'complete.info')):
                        stringAllInterruptedPatternsExhaustive.append(line)
                  try:
                     exhaustive_report.exhaustive_report(line,args.redo)
                  except:
                      print "COULDN'T REPORT THIS ONE! ERROR!"
                print "Exhaustive finished!"
        
        with open('interrupted_furer.info') as f:
           for furerInterrupted in stringAllInterruptedPatternsFurer:
               f.write(furerInterrupted+"\n")
        
        with open('interrupted_ffurer.info') as f:
           for furerInterrupted in stringAllInterruptedPatternsFurerAD:
               f.write(furerInterrupted+"\n")    
        
        with open('interrupted_ffurer.info') as f:
           for furerInterrupted in stringAllInterruptedPatternsFurerAD:
               f.write(furerInterrupted+"\n")    
                        
            
