This is the setup to read emails from the Grid (PanDa).


1. First download all the grid emails from the inbox. This is the link for Gmail (how you can download only grid emails):

https://webapps.stackexchange.com/questions/25689/how-to-export-selected-emails-from-gmail (read the second answer)

2. Once the grid emails are in mbox format, run the code:


python ReadMail.py -b (to write bash script) -p (to write text file with parameters for the broken jobs) -m (give the input mbox file name)


3. This should create two files: one bash script with all the retriable jobs, one text file with names and parameters of all the broken jobs. 
