import dns.resolver
result = dns.resolver.query('example.com', 'A')
for ipval in result:
    print('IP', ipval.to_text())
    
import socket
hostname, aliaslist, ipaddrlist = socket.gethostbyaddr("8.8.8.8")
print(hostname)
