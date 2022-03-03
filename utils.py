
CLP_BLACKLIST = ['CLP$', 'CLP', 'precio', 'internet', 'normal',
                 '$', '.', ',', '&nbsp;', '\r', '\n', '\t', '\xa0']

def remove_words(text, blacklist=CLP_BLACKLIST):
    for word in blacklist:
        text = text.replace(word, '')

    return text