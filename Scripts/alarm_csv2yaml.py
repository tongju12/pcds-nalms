# All data needs to be in a single csv file
# -> https://portal.frib.msu.edu/divisions/accsystems/preoperation/_layouts/15/WopiFrame2.aspx?sourcedoc=/divisions/accsystems/preoperation/Shared%20Documents/Working%20Documents/Alarms/alarm_ops-beastconfig.xlsx&action=default
#    Modify this Excel file, and check the PV column for duplicates. 
#    Export this spreadsheet as a csv file. 
#    Remove the first 3 header lines. 
#
# Run this file to get a new alarm_fe.yaml, then run alarmYaml2xml.py to create alarm_fe.xml
# Commit and push everything to alarm_fe 
#
# TS 05/25/18

fi = open('GMDXGMD.csv', 'r')
fo = open('GMDXGMD.yaml', 'w')

global padding

print ("Reading input file")
n=0
for i,line in enumerate(fi):
    n+=1
    #print "line {0} = {1}".format(i, line.split(','))
    lis = line.split(',')

    try: 
        int(lis[0]) # It's a line with indent # and branch name
        padding = " " *(4*int(lis[0]))
        fo.write('{0}\"{1}\":\n'.format(padding,lis[1].strip()))
    except:
        try: 
            if lis[0] == "#Indent":
                pass  # It's the header line
            if lis[13]:
                print ("Entry at line " + str(n) + " has extra commas in description or guidance")
            else: 
                pass
        except:
            try:
                fo.write('{0}  - pv: \"{1}\"\n'.format(padding,lis[2].strip()))
                fo.write('{0}    description: \"{1}\"\n'.format(padding,lis[3].strip()))
                fo.write('{0}    latching: {1}\n'.format(padding,lis[4].strip()))
                fo.write('{0}    delay: {1}\n'.format(padding,lis[5].strip()))
                # if lis[6]:
                #     fo.write('{0}    filter: {1}\n'.format(padding,lis[6].strip()))
                # if lis[7]:
                #     fo.write('{0}    guidance:\n'.format(padding))
                #     fo.write('{0}        title: \"Guidance\"\n'.format(padding))
                #     fo.write('{0}        details: \"{1}\"\n'.format(padding,lis[7].strip()))
            except:
                pass
    
print ("Finished reading file")

fi.close()
fo.close()
