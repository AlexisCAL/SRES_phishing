from Levenshtein import *
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

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

subdomain = 'Bonjour, monde !'

# Make a blank image for the text, initialized to transparent text color
size = width, height = 500, 30
text = Image.new('RGB', size, (255,255,255))
# get a font
font = ImageFont.truetype('DejaVuSansMono.ttf', 12)
# get a drawing context
draw = ImageDraw.Draw(text)
draw.text((5, 9), subdomain, font=font, fill=(0,0,0))

text.save('images/tmp.jpg')
