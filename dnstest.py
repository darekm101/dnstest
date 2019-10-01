import dns.resolver
import socket
import time
import statistics as stats
import argparse
import sys

DEBUG = False


parser = argparse.ArgumentParser()
parser.add_argument('--net', help="Provide class C subnet to reverse lookup i.e. --net '10.10.10.0'")
parser.add_argument('--debug', help="Turn on debugging. i.e. --debug True")

args = parser.parse_args()

# #If ran without arugments, let's print help and exit. 
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.debug: 
    DEBUG = args.debug

subnet_octets = args.net.split(".")
subnet = subnet_octets[0] + "." + subnet_octets[1] + "." + subnet_octets[2] + "."
# Let's get inistance of our own resolvers that's based on system settings
resolver = dns.resolver.Resolver()
dns_servers = resolver.nameservers
print(f"Name servers in use: {dns_servers}")

# Setup some stat vars

reverse_lookup_times = []
forward_lookup_times = []

def reverse_lookup(ip):
    try: 
        result = socket.gethostbyaddr(ip)
        print(".", end="")
        name, _, _ = result
        return name
    except Exception as e:
        if DEBUG: print(f"No entry for {ip} Error: {e}")
        return False

def forward_lookup(host_name):
    start = time.time()
    try: 
        result = resolver.query(host_name)
        if DEBUG: print(f"{host_name} = {result}")
        return time.time() - start
    except Exception as e:
        if DEBUG: print(f"No entry for {host_name} Error: {e}")
        return False

def reset_stats():
    global reverse_lookup_times
    reverse_lookup_times = []
    global forward_lookup_times
    forward_lookup_times = []

host_list = []

for dns_server in dns_servers:

    resolver.nameservers = [dns_server]

    print("*" * 80)
    print(f"Inspecting DNS server: {resolver.nameservers}")
    
    print(f"Reverse DNS lookup on {subnet} space.")
    for i in range(0,255):
        start = time.time()
        result = reverse_lookup(subnet+str(i))
        if result:
            reverse_lookup_times.append(time.time() - start)
            if DEBUG: print("Device found at: ", subnet+str(i) + ":"+str(22) + f" {result}")
            host_list.append(result)

    for host in host_list:
        forward_lookup_times.append(forward_lookup(host))

    if host_list: 
            
        print(f"\n\nReverse Lookup Stats: ")
        print(f"Total: {len(reverse_lookup_times)}")
        print(f"Mean: {stats.mean(reverse_lookup_times)}")
        print(f"Max: {max(reverse_lookup_times)}")

        print(f"\nForward Lookup Stats: ")
        print(f"Total: {len(forward_lookup_times)}")
        print(f"Mean: {stats.mean(forward_lookup_times)}")
        print(f"Max: {max(forward_lookup_times)}")

        reset_stats()
    else:
        print("That network space did not return a single reversere lookup, try different network segmet.")

