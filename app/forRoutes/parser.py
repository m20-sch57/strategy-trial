#[website.net] - Website page
#__text__ - underlined text
#**text** - bold text
#`code` - code

Link_text = ['">']
def something_else_you_need(el, i, l):
    global Link_text
    if el_d['[']['bool'] and el != ']':
        Link_text[0] += el
    elif el != ']':
        Link_text[0] = '">'
    else:
        Link_text[0] += '</a>'
    if i >= l:
        Link_text[0] += '</a>'

#ocb - open (o) symbol, close (c) or both (b)
#bool - True: in, False: out
#anti - close symbol to open one and vice versa
#num - number of symbols: '*': { ..,'num': 3} => '***'

el_d = {
'_': {'ocb': 'b', 'mean': ['<u>', '</u>'], 'anti': '_', 'bool': False, 'num': 2}, 
'*': {'ocb': 'b', 'mean': ['<b>', '</b>'], 'anti': '*', 'bool': False, 'num': 2}, 
'`': { 'ocb': 'b', 'mean': ['<pre><code>', '</code></pre>'], 'anti': '`', 'bool': False, 'num': 1}, 
'[': { 'ocb': 'o', 'mean': ['<a href="'], 'anti': ']', 'bool': False, 'num': 1},
']': { 'ocb': 'c', 'mean': Link_text , 'anti': '[', 'num': 1, 'bool': False}}

def use_parser(el):
    if (el_d['`']['bool'] and el != '`') or (el_d['[']['bool'] and el != ']'):
        return False
    return True

def parser(text):
    text = easyParser(text)
    newtext = ''
    i = 0
    while i < len(text):
        something_else_you_need(text[i], i, len(text))
        if text[i] in el_d and use_parser(text[i]):
            el = text[i]
            q, plus = True, el_d[el]['num']
            for j in range(plus):
                if not(i + j < len(text) and text[i + j] == el):
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
                something_else_you_need('', i, len(text))
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
