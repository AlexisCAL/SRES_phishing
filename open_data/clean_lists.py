
exec(open('main.py').read())
extensions = sorted(set(extensions), key=str.lower)
words = sorted(set(words), key=str.lower)
officials = sorted(set(officials), key=str.lower)

ext = open('open_data/clean_ext', 'w')
for e in extensions:
    ext.write("%s\n" % e)
word = open('open_data/clean_word', 'w')
for w in words:
    word.write("%s\n" % w)
add = open('open_data/clean_add', 'w')
for a in officials:
    if 'http://' in a:
        a = a[7:]
    add.write("%s\n" % a)
