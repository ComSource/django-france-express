#!/usr/bin/env python

import sys,re
from django.template.defaultfilters import slugify
from decimal import Decimal as D

FRANCE_EXPRESS_THRESHOLD_WEIGHT = 100

def json_out( astr, is_first=False ):
    if not is_first:
        print ","
    print astr.replace("'","\"").replace("u\"","\""),

def main():
    """Quick and dirty script to generate fixtures (initial data) from france express flat file
    """
    
    if len(sys.argv) != 2:
        print "Usage: %s rate_file.txt" % sys.argv[0]
        sys.exit(2)
        
    ratefile = sys.argv[1]
    f = open(ratefile)
    data = f.readlines()
    json_p = '  {"pk": %d, "model": "france_express.%s", "fields": %s}'
    offer_p = re.compile(u'^;;(.*)$')
    zone_p = re.compile(u'^::Zone::(.*)$')
    weights_p = re.compile(u'^::Weights$')
    rates_p = re.compile(u'^::Rates$')
    
    offer_id = zone_id = dept_id = rate_id = 0

    print "["
    
    for i in range(0,len(data)):
        l = data[i].strip()
        printed = False
        
        # Skip empty lines or commentaries
        if not len(l) or l[0] == "#":
            continue

        # Offer
        if offer_p.match(l):
            offer_name = offer_p.match(l).group(1).strip()
            offer_slug = slugify(offer_name)
            offer_id += 1
            zones = []
            out = json_p % ( offer_id, "offer", { "name":offer_name })
            json_out( out, offer_id == 1 )
            
        # Zone
        elif zone_p.match(l):
            zone_name = u'%s-zone-%s' % (offer_slug,zone_p.match(l).group(1).strip())
            zone_id += 1
            zones.append(zone_id)
            out = json_p % ( zone_id, "zone", { "name":zone_name, "offer":offer_id })
            json_out( out )            

            # Department
            for dept in [ int(d) for d in data[i+1].split() ]:
                dept_id += 1
                out = json_p % ( dept_id, "department", { "number":dept, "zone":zone_id })
                json_out( out )
                                                    
        # Weights
        elif weights_p.match(l):
            # Ignore the last weight that is used for weights > 100kg
            weights = [ D(w) for w in data[i+1].split() ][:-1]

        # Rates
        elif rates_p.match(l):
            for z in range(len(zones)):
                prices  = [ D(p) for p in data[i+z+1].split()[:-1] ]
                t_price = D(data[i+z+1].split()[-1])
                # Consider also >100kg prices
                for w in range(0,40):
                    for r in range(len(weights)):                                        
                        rate_id += 1
                        out = json_p % ( rate_id, "rate", { "weight":"%.2f"%(w*FRANCE_EXPRESS_THRESHOLD_WEIGHT+weights[r]), "price":"%.2f"%(w*t_price+prices[r]), "zone":zones[z] })
                        json_out( out )                        
                                    
    print "]"
    f.close()
    

if __name__ == '__main__':
	main()
