########################################
####### run it like: 
####### python ReadMail.py -b (to write bash script) -p (to write text file with parameters for the broken jobs) -m (give the input mbox file name)
########################################
import mailbox, os, sys, time
import math, argparse

def main():
    
    ### get the arguments
    parser   = argparse.ArgumentParser()
    parser.add_argument('-b', dest='needBash', action='store_true')
    parser.add_argument('-p', dest='needTxt', action='store_true')
    parser.add_argument('-m', action="store", dest="mboxFileName")
    args = parser.parse_args()
    
    mbox           = mailbox.mbox(args.mboxFileName)
    writeBash      = args.needBash
    writeParameter = args.needTxt
    
    ### if write to bash, open the bash script
    if writeBash:
        myBash = open("pbookFromMail.sh","w")
        myBash.write("#!/bin/bash\n")
        myBash.write("pbook << EOF\n")
    
    #### preparing the output file name depending on the input file name
    fileInName    = args.mboxFileName
    withoutSuffix = fileInName.split('.mbox')[0]
    brokenJobs    = open(withoutSuffix+'.txt', 'w')
    brokenJob     = 0 
    unfinishedJob = 0 
    totalJobCount = 0 
    
    ### looping through each mail
    for message in mbox:
        ### count the number of mails
        totalJobCount = totalJobCount + 1
        #print "from   :", message['from']
        subjectLine    = message['subject']
        print "subject:", subjectLine 
        
        ### getting different parts of the subject line
        eachWord = subjectLine.split()
        taskId   = eachWord[3].split(':')[1]
        status   = eachWord[4].split('(')[1]
        doneJob  = eachWord[4].split('(')[1].split('/')[0]
        totalJob = eachWord[4].split('(')[1].split('/')[1]
        if message.is_multipart():
            content = ''.join(part.get_payload(decode=True) for part in message.get_payload())
        else:
            content = message.get_payload(decode=True)
            
        ### if there is a broken job, no point retrying it, rather it needs to be submitted fresh.
        if('Final Status : broken' in content): 
            brokenJobs.write("\n")
            brokenJobs.write("*****mail number  "+str(brokenJob)+" ************************\n")
            contentList = content.splitlines()
            print content
            for contentLine in contentList:
                if 'In  :' in contentLine:
                    print contentLine
                    brokenJobs.write(contentLine.split('In  :')[1]+'\n')
                if(writeParameter):
                    if 'Parameters :' in contentLine:
                        brokenJobs.write('----\n')
                        print contentLine
                        brokenJobs.write(contentLine+'\n')
            time.sleep(0)
            brokenJob += 1
            
        ### the job is not broken    
        else:
            
            #### the doneJob is less than the totalJob, these jobs can be retried. 
            if(int(doneJob)!=int(totalJob)):
                print "Task ID: ", taskId
                print "status: ", status
                print "number done: ", doneJob
                print "number total: ", totalJob
                print taskId,": ", status, ": ", doneJob, ": ", totalJob
                if writeBash:
                    myBash.write("retry("+taskId+")\n")
                unfinishedJob += 1
    
    ### close the bash script
    if writeBash:
        myBash.write("EOF")
        myBash.close()
        
    brokenJobs.close()
    print "Number of broken jobs: ", brokenJob
    print "Number of unfinished jobs: ", unfinishedJob
    print "Total number of jobs: ", totalJobCount
    
    
    
if __name__ == "__main__":
    main()
