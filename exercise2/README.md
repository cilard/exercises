# scanner.py
The utility is used to do port scan of devices on the network. The `target` can be specified as sinle IPv4 IP address or subnet in CIDR format. If used with /24 subnet target, it is possible to further limit devices to be scanned by using the `--`--range` parameter.

It also stores the results in a file `/tmp/scanner.db` which if is read when the program starts. Using the file a 'database' is being created by storing target IP addresses with respective listening ports. This allows for tracking of port status changes between subsequent runs. These changes are flagged as:

| Port status flag | Description|
| ---------------- | ---------- |
| `[No change]` | The port is open and it was also open in the previous run |
| `[New]` | First time the port showed up in the results |
| `[Closed]` | Port was open in previous run and now it is closed |

### Usage
```
usage: scanner.py [-h] [-r RANGE] target

positional arguments:
  target                specify the target to scan

optional arguments:
  -h, --help            show this help message and exit
  -r RANGE, --range RANGE
                        specify a range to scan (last octet of IP addr), e.g.
                        10:20 for x.x.x.20 - x.x.x.30
```

### Examples
Scan a host
```
$ python3 scanner.py 192.168.1.100
*Target - 192.168.1.100: Full scan results:*
Host: 192.168.1.100		Ports: 22/open/tcp [New]
```
Scan the same host again (httpd started)
```
$ python3 scanner.py 192.168.1.100
*Target - 192.168.1.100: Full scan results:*
Host: 192.168.1.100		Ports: 22/open/tcp [No change]
Host: 192.168.1.100		Ports: 80/open/tcp [New]
```
Scan network segment
```
$ python3 scanner.py 192.168.1.0/24 --range 100:110
*Target - 192.168.1.0/24: Full scan results:*
Host: 192.168.1.100		Ports: 22/open/tcp [No change]
Host: 192.168.1.100		Ports: 80/open/tcp [No change]
Host: 192.168.1.108		Ports: 22/open/tcp [New]
```
