import pytesseract
from Levenshtein import *
from PIL import Image, ImageDraw, ImageFont

filename = 'images/tmp'
ext = '.jpg'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

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
    text = Image.new('RGB', size, (255, 255, 255))
    font = ImageFont.truetype('DejaVuSerif.ttf', 16)
    draw = ImageDraw.Draw(text)
    draw.text((5, 7), subdomain.upper(), font=font, fill=(0, 0, 0))

    text.save(filename + ext)

# Compare Levenshtein distance of OCR with domain string
# Langues supportées: fra, eng, rus, chi_sim.


def cowd(domain, language='eng'):
    if language != 'eng':
        language = 'eng'
    subdomains = domain.split('.')
    d = 0
    for subdomain in subdomains:
        if subdomain == 'www':
            continue
        make_image(subdomain.upper())
        # Changer la langue en fonction de IPAPI ?
        ocr = pytesseract.image_to_string(Image.open(
            filename + ext), config='/usr/share/tessdata', lang=language)
        print(ocr)
        d = max(d, distance(subdomain.upper(), ocr))
    return d
