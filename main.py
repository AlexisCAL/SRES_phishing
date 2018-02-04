ext = open('open_data/clean_ext')
word = open('open_data/clean_word')
add = open('open_data/clean_add')

with ext as f:
    extensions = f.readlines()
extensions = [x.strip() for x in extensions]

with word as f:
    words = f.readlines()
words = [x.strip() for x in words]

with add as f:
    officials = f.readlines()
officials = [x.strip() for x in officials]


def feed_main(domains):
    for domain in domains:
        print(domain, "\n")
