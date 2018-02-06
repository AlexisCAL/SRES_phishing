from Levenshtein import *
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import pytesseract

filename = 'images/tmp.jpg'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract-ocr'

# distance_against_known_list
def dakl(domain):
    subdomains = domain.split('.')
    d = 0
    for subdomain in subdomains:
        if subdomain == 'www':
            continue
        tmp = 100
        for k in known_list:
            dl = distance(subdomain, k)
            if dl < tmp:
                tmp = dl
        d += tmp
    d /= len(subdomains)
    
    return d

def make_image(subdomain):
    size = width, height = 500, 30
    text = Image.new('RGB', size, (255,255,255))
    font = ImageFont.truetype('DejaVuSansMono.ttf', 12)
    draw = ImageDraw.Draw(text)
    draw.text((5, 9), subdomain, font=font, fill=(0,0,0))

    text.save(filename)

# Compare Levenshtein distance of OCR with domain string
# Langues supportées: fra, eng, rus, chi_sim.
def cowd(domain, language):
    subdomains = domain.split('.')
    for subdomain in subdomains:
        if subdomain == 'www':
            continue
        make_image(subdomain)
        
        ocr = pytesseract.image_to_string(Image.open(filename), lang=language, config='/usr/share/tessdata') # Changer la langue en fonction de IPAPI ?
        print(ocr)
        d = distance(subdomain, ocr)
    
    return d

cowd('www.text.bonjour', 'eng')
