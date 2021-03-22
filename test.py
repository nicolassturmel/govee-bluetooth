import time
import colorsys
from govee_btled import BluetoothLED
from flask import Flask
from flask import request
from threading import Thread, Lock

mutex = Lock()

t = 0
init = [0,0,0,0,0,0,0]
ledState = init
ledBrightness = init
hue = init
saturation = init
nextSend = init

app = Flask(__name__)
led = ['A4:C1:38:F0:67:FF','A4:C1:38:AA:AF:CD'] 
for i in range(0,len(led)):
    try:
        B = BluetoothLED(led[i])
        time.sleep(2)
        del B
    except:
        print('Could not connect to ' + led[i])
    print('trying ' + led[i])
    ledState[i] = 1
    ledBrightness[i] = 1
    hue[i] = 1
    saturation[i] = 1
    nextSend[i] = -5




def toHex(h):
    r = hex(round(255*h)).split('x')[-1]
    if len(r) == 1:
        r = "0" + r
    return r


print(toHex(0))

def setColor(hue,saturation,light):
    print(str(hue))
    print(str(saturation))
    rgb = colorsys.hsv_to_rgb(hue/360, saturation/100, light)
    col = "#"+toHex(rgb[0])+toHex(rgb[1])+toHex(rgb[2])
    print(col)
    return col


def sendThread():
    while True:
        global t
        global nextSend
        t = t + 1
        for i in range(0,len(nextSend)):
            if t == nextSend[i]:
                try:
                    B = BluetoothLED(led[i])
                    B.set_state(ledState[i] == 1 )
                    if ledState[0] == 1:
                            B.set_brightness(ledBrightness[i])
                            B.set_color(setColor(hue[i], saturation[i], ledBrightness[i] ))
                    time.sleep(1)
                    del B
                    time.sleep(1)
                except:
                    nextSend[i]+=5
                    print('Could not connect to ' + led[i])
        
        time.sleep(1)
        print(str(t))
        print(str(nextSend[0] ))
        if t > 100000:
            t = t - 100000
            for i in range(0,len(nextSend)):
                nextSend[i] = nextSend[i] - 100000


x = Thread(target=sendThread, args=())
x.start()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/state/<int:id>', methods=['GET'])
def getState(id):
    print(str(id))
    if id >= 0 and len(led) > id:
        return str(ledState[id] )
    else:
        return ""

@app.route('/on/<int:id>', methods=['GET'])
def on(id):
    if id >= 0 and len(led) > id:
        ledState[id] = 1
        nextSend[id] = t + 2
        return str(ledState[id] )
    else:
        return ""

@app.route('/off/<int:id>', methods=['GET'])
def off(id):
    if id >= 0 and len(led) > id:
        ledState[id] = 0
        nextSend[id] = t + 2
        return str(ledState[id] )
    else:
        return ""
    

@app.route('/getBrightness/<int:id>', methods=['GET'])
def getBrightness(id):
    b = int(request.args.get("brightness"))
    print(b)
    if id >= 0 and len(led) > id:
        ledBrightness[id] = b/100
        nextSend[id] = t + 2
        return str(ledBrightness[id] )
    else:
        return ""

@app.route('/brightness/<int:id>', methods=['GET'])
def brightness(id):
    if id >= 0 and len(led) > id:
        return str(round(100*ledBrightness[id]) )
    else:
        return ""

@app.route('/setHue/<int:id>', methods=['GET'])
def setHue(id):
    b = int(request.args.get("hue"))
    print(b)
    if id >= 0 and len(led) > id:
        hue[id] = b
        nextSend[id] = t + 2
        return str(hue[id] )
    else:
        return ""
    

@app.route('/getHue/<int:id>', methods=['GET'])
def getHue(id):
    if id >= 0 and len(led) > id:
        return str(round(hue[id]) )
    else:
        return ""

@app.route('/setSaturation/<int:id>', methods=['GET'])
def setSaturation(id):
    b = int(request.args.get("saturation"))
    print(b)
    if id >= 0 and len(led) > id:
        saturation[id] = b
        nextSend[id] = t + 2
        return str(saturation[id] )
    else:
        return ""
    

@app.route('/getSaturation/<int:id>', methods=['GET'])
def getSaturation(id):
    if id >= 0 and len(led) > id:
        return str(round(saturation[id]) )
    else:
        return ""

if __name__ == '__main__':
    app.run(host="0.0.0.0")
