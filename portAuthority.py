import subprocess
import datetime
import sys

date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

if len(sys.argv) < 2:
        print 'Missing argument. Please provide a network list file\n'
        print 'e.g. python portAuthority.py networks.txt'

try:
        zmapBin = subprocess.check_output(['which', 'zmap']).strip() + ' '
        print 'zmap was found at:\n' + zmapBin
except:
        print 'zmap was not found in your PATH, quitting'
        exit()

port = raw_input('Enter port or port range to scan\ne.g. 1234 or 1234-1299\n:')

with open(sys.argv[1], 'r') as networksFile:
                for network in networksFile:
                        netname = network[0:8]
                        outFile = date + '.' + port + '.' + netname + '.zmap'
                        print 'output file can be tailed with:\ntail -f '+ outFile
                        zmapOptions = ' -p ' + port + ' -o ' + outFile + ' -B 1M -s 53 -v 4 '
                        fullCommand = zmapBin + zmapOptions + network.strip()
                        print fullCommand + ' RUNNING \n'
                        subprocess.check_output(fullCommand, shell=True)

networksFile.close()
print 'Scanning complete\n'
print 'find *.zmap | grep ' + port + ' | xargs cat | uniq -u | sort'
exit()
