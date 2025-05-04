import math
#Math is needed for logarithms. Logarithms are needed for calculating number of bits needed for a given network requirement.

#Program Inputs
ip = input("Enter an IP address: ")

CIDR = "/0"
hosts = 0
subnets = 0

initial = input(
    "Are you going to use:\n1. Custom CIDR\n2. Host Requirements\n3. Subnet Requirements\n4. Host and Subnet Requirements\n"
)
if initial == "1":
    CIDR = input("Enter the Custom CIDR: ")
elif initial == "2":
    hosts = input("Enter the number of hosts per subnet: ")
elif initial == "3":
    subnets = int(input("Enter the number of subnets you would like: "))
elif initial == "4":
    hosts = int(input("Enter the number of hosts per subnet: "))
    subnets = int(input("Enter the number of subnets you would like: "))

default = 0
defaultCDR = 0
#Splitting IP Address and CIDR
ip = ip.split(".")

CIDR = CIDR.replace("/", "")


def classification(ip):
    if int(ip[0]) >= 0 and int(ip[0]) <= 127:
        return "Class A"
    elif int(ip[0]) >= 128 and int(ip[0]) <= 191:
        return "Class B"
    elif int(ip[0]) >= 192 and int(ip[0]) <= 223:
        return "Class C"
    elif int(ip[0]) >= 224 and int(ip[0]) <= 239:
        return "Class D"
    else:
        return "Class E"


IpClass = classification(ip)

if classification(ip) == "Class A":
    default = "255.0.0.0",
    defaultCDR = 8
elif classification(ip) == "Class B":
    default = "255.255.0.0",
    defaultCDR = 16
elif classification(ip) == "Class C":
    default = "255.255.255.0",
    defaultCDR = 24
elif classification(ip) == "Class D":
    default = "255.255.255.255",
    defaultCDR = 32

def calculate_CIDR(num_hosts):
    num_hosts = int(num_hosts)
    host_bits = 0
    while (1 << host_bits) <= num_hosts + 2:
        host_bits += 1

    network_bits = 33 - host_bits  # 33 bits, as we are always one number short of what it should be.
    return network_bits


def subnetmask(CIDR):
    CIDR = int(CIDR)
    mask = [0, 0, 0, 0]
    for i in range(CIDR):
        mask[i // 8] = mask[i // 8] + (128 >> (i % 8))
    return mask


#Network Requirements

NetworkBits = calculate_CIDR(hosts)
strNetworkBits = f"/{calculate_CIDR(hosts)}"
    
if CIDR == "0":
    bits_borrowed = int(NetworkBits - defaultCDR)
else:
    bits_borrowed = int(NetworkBits - int(CIDR))


#If and only if the user chooses to use subnet requirements or subnet and hosts, this will run.
def network_requirement(subnets):
  subnets = subnets
  customCIDR = 0
  bits_borrowed = math.ceil(math.log(subnets,2)) #Power of 2 chart, finding number of bits needed. So, this is number of bits borrowed.
  if classification(ip) == "Class A":
     customCIDR= 8 + bits_borrowed
  elif classification(ip) == "Class B":
     customCIDR= 16 + bits_borrowed
  elif classification(ip) == "Class C":
    customCIDR= 24 + bits_borrowed
  elif classification(ip) == "Class D":
     customCIDR= 14 + bits_borrowed
  else:
    return "Error"
  return customCIDR, bits_borrowed 

if initial =="1":
    print(f"IP Address: {ip}\n, Class: {IpClass}\n, Default Subnet Mask: {default}\n, Default/Given CIDR: {defaultCDR}\n, Subnet Mask: {subnetmask(CIDR)}\n, Custom CIDR: /{CIDR}\n bits borrowed: {abs(defaultCDR - int(CIDR))}\n Total Network Bits: {CIDR}\n Total Host Bits: {32 - int(CIDR)}\n")

if initial == "3":
  NetworkBits = network_requirement(subnets)[0]
  bits_borrowed = network_requirement(subnets)[1]
if initial == "4":
      NetworkBits = network_requirement(subnets)[0]
      bits_borrowed = network_requirement(subnets)[1]

if initial == "2" or "3" or "4":
    print(f"IP Address: {ip}\n, Class: {IpClass}\n, Default Subnet Mask: {default}\n, Default/Given CIDR: {defaultCDR}\n, Subnet Mask: {subnetmask(NetworkBits)}\n, Custom CIDR: /{NetworkBits}\n bits borrowed: {bits_borrowed}\n Total Network Bits: {NetworkBits}\n Total Host Bits: {32 - int(NetworkBits)}\n")
else:
    print("Error: Invalid Input")
