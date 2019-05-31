#[website.net] - Website page
#__text__ - underlined text
#**text** - bold text
#`code` - code

Link_text = ['">']
def something_else_you_need(el):
    global Link_text
    if el_d['[']['bool'] and el != ']':
        Link_text[0] += el
    elif el != ']':
        Link_text[0] = '">'
    else:
        Link_text[0] += '</a>'

el_d = {
'_': {'ocb': 'b', 'mean': ['<u>', '</u>'], 'anti': '_', 'bool': False, 'f': ['_', 2]}, 
'*': {'ocb': 'b', 'mean': ['<b>', '</b>'], 'anti': '*', 'bool': False, 'f': ['*', 2]}, 
'`': { 'ocb': 'b', 'mean': ['<pre><code>', '</code></pre>'], 'anti': '`', 'bool': False, 'f': ['`', 1]}, 
'[': { 'ocb': 'o', 'mean': ['<a href="'], 'anti': ']', 'bool': False, 'f': ['[', 1]},
']': { 'ocb': 'c', 'mean': Link_text , 'anti': '[', 'f': [']', 1]}}

def use_parser(el):
    if (el_d['`']['bool'] and el != '`') or (el_d['[']['bool'] and el != ']'):
        return False
    return True

def parser(text):
    text = easyParser(text)
    newtext = ''
    i = 0
    while i < len(text):
        something_else_you_need(text[i])
        if text[i] in el_d and use_parser(text[i]):
            el = text[i]
            q, plus = True, el_d[el]['f'][1]
            for j in range(plus):
                if not(i + j < len(text) and text[i + j] == el_d[el]['f'][0]):
                    q = False
            if q:
                if el_d[el]['ocb'] == 'b':
                    if el_d[el]['bool']:
                        newtext += el_d[el]['mean'][1]
                    else:
                        newtext += el_d[el]['mean'][0]
                    el_d[el]['bool'] = not el_d[el]['bool']
                elif el_d[el]['ocb'] == 'o':
                    if not el_d[el]['bool']:
                        newtext += el_d[el]['mean'][0]
                        el_d[el]['bool'] = True
                elif el_d[el]['ocb'] == 'c':
                    if el_d[el_d[el]['anti']]['bool']:
                        newtext += el_d[el]['mean'][0]
                        el_d[el_d[el]['anti']]['bool'] = False
                i += plus
            else:
                newtext += text[i]
                i += 1
        else:
            newtext += text[i]
            i += 1
        
    for el in el_d:
        if el_d[el]['ocb'] in ['o', 'b']:
            if el_d[el]['bool']:
                newtext += el_d[el_d[el]['anti']]['mean'][-1]
                el_d[el]['bool'] = False
    return newtext

def easyParser(text):
    newtext = ''
    for el in text:
        if el == '<':
            newtext += '&lt;'
        elif el == '>':
            newtext += '&gt;'
        else:
            newtext += el
    return newtext
