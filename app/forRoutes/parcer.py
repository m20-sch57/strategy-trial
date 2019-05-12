#[website.net] - Website page
#__text__ - underlined text
#**text** - bold text

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
                add = '<a href="http://' + text[i+1:i+j+1] + '">' + text[i+1:i+j+1] + '</a>'
            if symbol == '__':
                add = '<u>' + text[i+2:i+j+1] + '</u>'
                j += 1
            if symbol == '**':
                add = '<b>' + text[i+2:i+j+1] + '</b>'
                j += 1
        else:
            add = '[SOMETHING IS WRONG]'
    else:
        add = text[i]
    return [add, i + j + 1]

def parcer(text):
    len_text, i = len(text), 0
    newtext = ''
    while i < len_text:
        if text[i] == '<':
            newtext += '"<"'
        elif text[i] == '>':
            newtext += '">"'
        elif text[i] == '[' or (i + 1 < len_text and (text[i] + text[i+1] in ['**', '__'])):
            symbol = text[i]
            if text[i] in ['*', '_']:
                symbol += text[i]
            list_n = addText(text, i, symbol)
            newtext += list_n[0]
            i = list_n[1]
        else:
            newtext += text[i]
        i += 1
    return newtext

