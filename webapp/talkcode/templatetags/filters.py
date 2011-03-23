from django import template
register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def rate_chart(rate):
    output = ''
    if rate != None:
        for r in range(10-rate):
            output += '<div class="red box"></div>'
        for r in range(rate):
            output += '<div class="green box"></div>'
    else:
        for r in range(10):
            output += '<div class="yellow box"></div>'
    return output

@register.filter
def rate_img(topic):
    rate = topic.rate()
    print rate
    if rate == None:
        return 'yellow.png'
    elif rate > 0:
        return 'green.png'
    else:
        return 'red.png'
        
@register.filter
def colorize(atom):
    if atom.quality == 1:
        return 'green'
    elif atom.quality == -1:
        return 'red'
    else:
        return 'yellow'