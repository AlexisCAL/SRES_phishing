import pytesseract
from Levenshtein import *
from PIL import Image, ImageDraw, ImageFont

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # -ocr'

# distance_against_known_list


def dakl(domain, words):
    subdomains = domain.split('.')
    d = 0
    for subdomain in subdomains:
        if subdomain == 'www':
            continue
        tmp = 100
        for k in words:
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

    return text
    # text.save(filename + ext)

# Compare Levenshtein distance of OCR with domain string
# Langues supportées: fra, eng, rus, chi_sim.


def cowd(domain, language='eng'):
    subdomains = domain.split('.')
    d = 0
    for subdomain in subdomains:
        if subdomain == 'www':
            continue
        img = make_image(subdomain.upper())
        # Changer la langue en fonction de IPAPI
        ocr = pytesseract.image_to_string(img, config='/usr/share/tessdata', lang=language)  # lang=language. On ne supporte actuellement que l'anglais.
        d = max(d, distance(subdomain.upper(), ocr))
    return d
