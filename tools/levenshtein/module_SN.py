from Levenshtein import *

# distance_against_known_list
def dakl(domain):
    subdomains = domain.split('.')
    liste_connue = words + extensions
    d = 0
    for subdomain in subdomains:
        if subdomain == 'www':
            continue
        tmp = 100
        for l in liste_connue:
            dl = distance(subdomain, l)
            if dl < tmp:
                tmp = dl
        d += tmp
    d /= len(subdomains)
    
    return d

# Compare Levenshtein distance of OCR with domain string
#def cowd(domain):
    #subdomains = domain.split('.')
    #for subdomain in subdomains:
        #ocr = OCR(image(subdomain)) # Changer la langue en fonction de IPAPI ?
        #d = distance(subdomain, ocr)
    
    #return d   
