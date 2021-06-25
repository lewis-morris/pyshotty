# flask-screenshot

## A firefox selenium based screenshot package for use with flask  

Error while running selenium in a flask route brought me to create this - thinking that running as a subprocess might fix things.

Although that want the case, now I have a condensed easy format to grab website screenshots

## Prerequisites 

* Ubuntu 
* Firefox   `sudo apt-get install firefox`
* geckodriver `sudo apt-get install firefox-geckodriver`

## Features

* Grab screenshots from any website (in .png format)
* Choose browser size (essentially screenshot size)


## Installation

Download and install can be done through PyPi

```
pip install pyshotty
```
or

```python
git clone https://github.com/lewis-morris/pyshotty
cd pyshotty 
pip install -e .
```

## Pending Features

* Alternative image formats
* grab via Chrome selenium
* passing command line parameters

## How to use

### Minimal working example

```python

from pyshotty import Firefox
screen = Firefox("www.google.com")
filename = screen.run()

```

![Image](examples/tempscreenshot.png)


## Contact

If you have any issues or just want to chat you can always email me at lewis.morris@gmail.com or open an issue.
