"""
Defines a service for generating random words from romance language phonics.
Word model is largely inspired by Korean syllable constructs, but parameters
(including weights for vowel-like and consonant-like characters, and other
statistical inputs) can be adjusted by modifying module-level variables.
"""

import os
import random
import flask
from gevent import pywsgi
from numpy import random as npr

MOD_PATH, _ = os.path.split(os.path.abspath(__file__))
_, MOD_NAME = os.path.split(MOD_PATH)
APP = flask.Flask(MOD_NAME)
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# model parameters, "initialized" by scrabble count
VOWEL_LIKES = {
    "a": 9,
    "e": 12,
    "i": 9,
    "o": 8,
    "u": 4,
    "ei": 1,
    "ie": 1,
    "oo": 1,
    "ou": 1,
    "ui": 1
}
CONSONANT_LIKES = {
    "b": 2,
    "c": 2,
    "d": 4,
    "f": 2,
    "g": 3,
    "h": 2,
    "j": 8,
    "k": 1,
    "l": 4,
    "m": 2,
    "n": 6,
    "p": 2,
    "r": 6,
    "s": 4,
    "t": 6,
    "v": 2,
    "w": 2,
    "x": 1,
    "z": 1,
    "qu": 1,
    "th": 1,
    "ch": 1,
    "ck": 1,
    "ph": 1,
    "sh": 1
}
SYLLABLES_MODE = 3
PNULL_CONSONANTS = 0.3

def chooseFromMap(drawMap):
    """
    Given a "drawMap" dictionary, returns a key. Values in the map are
    probability densities, used to construct a discrete CDF against which a
    draw is performed.
    """
    cumulative = {}
    prevVal = 0
    keys = list(drawMap.keys())
    for k in keys:
        v = drawMap[k]
        cumulative[k] = prevVal + v
        prevVal += v
    # prevVal now has the maximum value
    draw = random.random() * prevVal
    prevVal = 0
    for i, k in enumerate(keys):
        v = cumulative[k]
        if prevVal <= draw and draw < v:
            return k
        if i == len(keys) - 1:
            return k
        prevVal = v
    raise Exception("Should not have reached past the final possibility")

def getSyllable():
    """
    Constructs a syllable by aggregating a consonant-like / vowel-like /
    consonant-like sequence. There is a probablity that the constant-like
    sequences will instead draw a "null" and will therefore be empty. Specific
    sequences are taken from the "draw maps" defined in module level variables
    CONSONANT_LIKES and VOWEL_LIKES.
    """
    c1 = ""
    v = ""
    c2 = ""
    if PNULL_CONSONANTS < random.random():
        c1 = chooseFromMap(CONSONANT_LIKES)
    v = chooseFromMap(VOWEL_LIKES)
    if PNULL_CONSONANTS < random.random():
        c2 = chooseFromMap(CONSONANT_LIKES)
    return c1 + v + c2
    
def getWord():
    """
    Constructs a word by aggregating a number of syllables. The specific number
    of syllables is the result of a poisson draw against the lamba (peak) value
    defined by SYLLABLES_MODE, with adjustments to ensure 0 is not drawn.
    """
    word = ""
    nSyllables = npr.poisson(SYLLABLES_MODE - 1) + 1 # prevents a draw of 0
    for _ in range(nSyllables):
        word += getSyllable()
    return word

@APP.route("/")
def index():
    """
    Returns a word as a byte-encoded Flask response.
    """
    return getWord().encode(), 200, {
        "Content-Type": "text/plain"
    }

def main():
    """
    Starts a gevent-based WSGI server for the module's Flask application.
    """
    print("Serving '%s' service at %s:%u..." % (MOD_NAME, SERVER_HOST, SERVER_PORT))
    pywsgi.WSGIServer((SERVER_HOST, SERVER_PORT), APP).serve_forever()

if __name__ == "__main__":
    main()
