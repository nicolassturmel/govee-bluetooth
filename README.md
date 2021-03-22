# govee-bluetooth
Python script to control gobée bluetooth strips

Tested with model 8081

## Install
```
pip3 install flask  
pip3 install -U git+https://github.com/Freemanium/govee_btled
```

## Config

Put your mac addresses in the led array line 19

## Use

With the homebridge http lightbulb plugin

```
{
    "accessory": "HTTP-LIGHTBULB",
    "name": "Light",
    "onUrl": "http://localhost:5000/on/0",
    "offUrl": "http://localhost:5000/off/0",
    "statusUrl": "http://localhost:5000/state/0",
    "brightness": {
        "setUrl": "http://localhost:5000/getBrightness/0?brightness=%s",
        "statusUrl": "http://localhost:5000/brightness/0"
    },
    "hue": {
        "setUrl": "http://localhost:5000/setHue/0?hue=%s",
        "statusUrl": "http://localhost:5000/getHue/0"
    },
    "saturation": {
        "setUrl": "http://localhost:5000/setSaturation/0?saturation=%s",
        "statusUrl": "http://localhost:5000/getSaturation/0"
    }
}
```

where /0 is the light index in the led array