import subprocess
import datetime
import sys
from netaddr import IPNetwork

netcount = 0
ipcount = 0
errList = []
date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

if len(sys.argv) < 2:
        print 'Missing argument. Please provide a network list file\n'
        print 'e.g. python portAuthority.py networks.txt'

try:
        zmapBin = subprocess.check_output(['which', 'zmap']).strip()
        print 'zmap was found at:\n' + zmapBin
except:
        print 'zmap was not found in your PATH, quitting'
        exit()

port = raw_input('Enter port or port range to scan\ne.g. 1234 or 1234-1299\n:')

with open(sys.argv[1], 'r') as networksFile:
                for network in networksFile:
                        netcount = netcount +1
                        ip = IPNetwork(network)
                        ipcount = ipcount + ip.size 

print 'Total number of networks to be scanned: ' + str(netcount)
print 'Total number of IPs to be scanned: ' + ("{:,}".format(ipcount));

choice = raw_input('Would you like to continue? Y/N ').lower()
if 'n' in choice:
        exit()

with open(sys.argv[1], 'r') as networksFile:
        for network in networksFile:
                netname = network[0:8].strip('.')
                outFile = '{0}.{1}.{2}.zmap'.format(date, port, netname)
                zmapOptions = ' -p {0} -o {1} -B 1M -s 53 -v 4 '.format(port, outFile)
                fullCommand = zmapBin + zmapOptions + network.strip()
                print fullCommand + ' RUNNING \n'
                try:
                        subprocess.check_output(fullCommand, shell=True)
                except subprocess.CalledProcessError as e:
                        errList.extend(e.output)
                        continue

networksFile.close()
print 'Scanning complete\n'
print 'The following errors where caught:\n'
for error in errList:
        print error
print 'find *.zmap | grep ' + port + ' | xargs cat | uniq -u | sort'
exit()