# ARP/MAC
# modify or filter characters from mac address
# mac address normalizer

import re
mac = 'ffff.ffff.ffff'

mac1 = re.sub('[.]', '', mac)

'-'.join(mac1[i:i+2] for i in range(0, len(mac1), 2))
