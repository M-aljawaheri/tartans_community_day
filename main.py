# Import necessary modules
from cmu_graphics import *
import joystick
import sys
import random
import time

# Define the Numpad class
class Numpad:
    def __init__(self, app):
        self.app = app
        self.buttons = [str(i) for i in range(1, 10)] + ['0']
        self.selectedButtonIndex = 0
        self.app.text = ''

    def draw(self):
        for i, button in enumerate(self.buttons):
            x = 150 + (i % 3) * 100
            y = 200 + (i // 3) * 100
            if i == self.selectedButtonIndex:
                fillColor = 'yellow'
            else:
                fillColor = 'white'
            drawRect(x, y, 80, 80, fill=fillColor)
            drawLabel(button, x + 40, y + 40, size=30)

    def moveSelection(self, dx, dy):
        row = self.selectedButtonIndex // 3
        col = self.selectedButtonIndex % 3
        row = min(max(row + dy, 0), 3)
        col = min(max(col + dx, 0), 2)
        self.selectedButtonIndex = row * 3 + col

    def getCurrentSelection(self):
        return self.buttons[self.selectedButtonIndex]

def handleKeyPress(app, key):
    pass

# Define global functions for joystick handling
def onJoyPress(app, button, joystick):
    if button == '0':  # 'X' button
        app.currentNumber = app.currentNumber[:-1]
    elif button == '1':  # 'A' button
        app.currentNumber += app.numpad.getCurrentSelection()
    elif button == '2':  # 'B' button
        checkNumber(app)
    elif button == '5':
        sys.exit(0)

def onJoyButtonHold(app, buttons, joystick):
    if 'H0' in buttons:  # Up
        app.numpad.moveSelection(0, -1)
    elif 'H2' in buttons:  # Down
        app.numpad.moveSelection(0, 1)
    if 'H3' in buttons:  # Left
        app.numpad.moveSelection(-1, 0)
    elif 'H1' in buttons:  # Right
        app.numpad.moveSelection(1, 0)

def checkNumber(app):
    if app.currentNumber == '1176':
        app.showQR = True
        app.qrStartTime = time.time()
    else:
        app.text = "Wrong number. Try again!"
        app.currentNumber = ''

def onAppStart(app):
    app.numpad = Numpad(app)
    app.currentNumber = ''
    app.showQR = False
    app.qrStartTime = 0
    app.qrImages = ['QR_corridor.png'] # ['QR1.png', 'QR2.png', 'QR3.png', 'QR4.png']

def redrawAll(app):
    if app.showQR:
        currentTime = time.time()
        if currentTime - app.qrStartTime > 30:
            app.showQR = False
            app.currentNumber = ''
        else:
            qrIndex = int((currentTime - app.qrStartTime) / 7.5) % 4
            drawImage(app.qrImages[qrIndex], 200, 200)
    else:
        app.numpad.draw()
        drawLabel(f"Enter Number: {app.currentNumber}", app.width//2, 100, size=30)
        drawLabel(f"X to backspace {app.currentNumber}", app.width - app.width//7, 200, size=30)
        drawLabel(f"A to enter {app.currentNumber}", app.width - app.width//7, 240, size=30)
        drawLabel(f"B to submit {app.currentNumber}", app.width - app.width//7, 280, size=30)
        if app.text:
            drawLabel(app.text, app.width//2, 150, size=20)

# Initialize the app
runApp(width=800, height=600)