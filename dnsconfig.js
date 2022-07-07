// Defaults:
function includeSOA() { return SOA("@", "resolv-au1sr-1.thefathacker.net.", "thefathacker.thefathacker.tech.", 3600, 600, 604800, 1440) }

resolv_servers = [
    NAMESERVER("resolv-au1sr-1.thefathacker.net."),
    NAMESERVER("resolv-au1sr-2.thefathacker.net.")
]

// Providers:

var REG_NONE = NewRegistrar('none');    // No registrar.
var DNS_BIND = NewDnsProvider('bind');  // ISC BIND.

// Domains:

D(REV('2403:580b:a316::/48'), REG_NONE, DnsProvider(DNS_BIND),
    resolv_servers,
    includeSOA()
);
D(REV('172.31.0.0/16'), REG_NONE, DnsProvider(DNS_BIND),
    resolv_servers,
    includeSOA()
);

require("./netbox.dnscontrol.js")