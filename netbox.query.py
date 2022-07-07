import pynetbox
import json
import ipaddress
import types
import subprocess

with open("./netbox.settings.json") as f:
    nb_conf = json.load(f)

nb = pynetbox.api(nb_conf["url"], token=nb_conf["key"])

rzones = []
dnscontrol_data = []

tags = types.SimpleNamespace()
for tag in nb.extras.tags.all():
    if(tag.name == "DNS"): tags.dns = tag

for tenant in nb.tenancy.tenants.all():
    if(tenant.name == "The Fat Hacker"): thefathacker = tenant
    
for prefix in nb.ipam.prefixes.all():
    if(tags.dns in prefix.tags and prefix.tenant == thefathacker): rzones.append(prefix)

for z in rzones:
    rzonedata = []
    for ip in nb.ipam.ip_addresses.all():
        if(ip.family.value == z.family.value):
            if(ipaddress.ip_address(ip.address.split("/")[0]) in ipaddress.ip_network(z) and ip.tenant == thefathacker):
                if(ip.dns_name != ""):
                    dns = ip.dns_name
                    if(dns[-1] != "."): dns = dns + "."
                    rzonedata.append("PTR(REV('" + ip.address.split("/")[0] + "'), '" + dns + "')")
    dnscontrol_data.append("D_EXTEND(REV('"+z.prefix+"'), " + ",\n".join(rzonedata)+")\n")

with open("./netbox.dnscontrol.js", "w") as f:
    for data in dnscontrol_data:
        f.write(data)
        f.flush()
    f.close()


subprocess.run(['dnscontrol','push'])