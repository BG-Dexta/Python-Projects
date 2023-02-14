text = "Yesterday I saw a wild NOUN. He was very ADJECTIVE and couldn't VERB. NOUN wants to VERB him ADVERB."
keywords = ['NOUN', 'ADJECTIVE', 'ADVERB', 'VERB']


def obr(t):
    for i in keywords:
        if i in t:
            nt = input('replace %s with: ' % i)
            return t.replace(i, nt)
    return t

fileText = open('text.txt', 'w')
fileText.write(text)
fileText.close()

fileText = open('text.txt', 'r')
oldText = fileText.read()
fileTextNew = open('newText.txt', 'w')

fileTextNew.write(' '.join([obr(i) for i in oldText.split()]))

fileText.close()
fileTextNew.close()
