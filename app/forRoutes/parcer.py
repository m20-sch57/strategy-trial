#<website.net> - Website page
#__text__ - underlined text

"""
сначала орределение ссылок
"""
stringlong = 60
linenumber = 0
def anti(symbol):
    if symbol == '[':
        return ']'
    else:
        return symbol

def addText(text, i, symbol):
    add = ''
    j = text[i+1:].find(anti(symbol))
    if j != -1:
        if text[i:i+j+1].find('<') == -1:
            if symbol == '[':
                add = '<a href="' + text[i+1:i+j+1] + '">' + text[i+1:i+j+1] + '</a>'
                j += 1
            if symbol == '__':
                add = '<u>' + text[i+2:i+j+1] + '</u>'
                j += 2
        else:
            add = '[SOMETHING IS WRONG]'
    else:
        add = text[i]
        j = 0
    return [add, i + j]

def parcer(text):
    len_text, i = len(text), 0
    newtext = ''
    while i < len_text:
        if text[i] == '<':
            newtext += '"<"'
        elif text[i] == '>':
            newtext += '">"'
        elif text[i] == '[' or (i + 1 < len_text and text[i] + text[i+1] == '__'):
            symbol = text[i]
            if text[i] == '_':
                symbol += '_'
            list_n = addText(text, i, symbol)
            newtext += list_n[0]
            i = list_n[1]
        else:
            newtext += text[i]
        i += 1
        print(newtext)
    return newtext

