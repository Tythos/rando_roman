Rando Roman
===========
   
Defines a service for generating random words from romance language phonics.
Word model is largely inspired by Korean syllable constructs, but parameters
(including weights for vowel-like and consonant-like characters, and other
statistical inputs) can be adjusted by modifying module-level variables.

When invoked from the command line, the generator is hosted as a WSGI
application that responds to root-path queries with a single random word::

    > python __init__.py

    > curl http://localhost:8000

Specific parameters are given in subsequent sections, titled for the
corresponding module-level variables.

.. contents::

VOWEL_LIKES
-----------

Vowels in this model define the center element of a syllable. The statistical
distribution of vowels in this model are defined by a "draw map" whose values
are first based from Scrabble tile counts (or weights), with single-count
entries added for some of the more common multi-letter vowel-like sounds.
Specific default values are presented in the following table.

+------------+--------+
| Characters | Weight |
+============+========+
| a          | 9      |
+------------+--------+
| e          | 12     |
+------------+--------+
| i          | 9      |
+------------+--------+
| o          | 8      |
+------------+--------+
| u          | 4      |
+------------+--------+
| ei         | 1      |
+------------+--------+
| ie         | 1      |
+------------+--------+
| oo         | 1      |
+------------+--------+
| ou         | 1      |
+------------+--------+
| ui         | 1      |
+------------+--------+

CONSONANT_LIKES
---------------

Consonants in this model define the "edge" elements of a syllable. The
statistical distribution of consonants in this model are defined by a "draw
map" whose values are first based from Scrabble tile counts (or weights), with
single-count entries added for some of the more common multi-letter
consonant-like sounds. Specific default values are presented in the following
table.

Note that consonants, when generating a syllable, have a probability of being
"null" or empty. See "PNULL_CONSONANTS" for more details.

+------------+--------+
| Characters | Weight |
+============+========+
| b          | 2      |
+------------+--------+
| c          | 2      |
+------------+--------+
| d          | 4      |
+------------+--------+
| f          | 2      |
+------------+--------+
| g          | 3      |
+------------+--------+
| h          | 2      |
+------------+--------+
| j          | 8      |
+------------+--------+
| k          | 1      |
+------------+--------+
| l          | 4      |
+------------+--------+
| m          | 2      |
+------------+--------+
| n          | 6      |
+------------+--------+
| p          | 2      |
+------------+--------+
| r          | 6      |
+------------+--------+
| s          | 4      |
+------------+--------+
| t          | 6      |
+------------+--------+
| v          | 2      |
+------------+--------+
| w          | 2      |
+------------+--------+
| x          | 1      |
+------------+--------+
| z          | 1      |
+------------+--------+
| qu         | 1      |
+------------+--------+
| th         | 1      |
+------------+--------+
| ch         | 1      |
+------------+--------+
| ck         | 1      |
+------------+--------+
| ph         | 1      |
+------------+--------+
| sh         | 1      |
+------------+--------+

SYLLABLES_MODE
--------------

The number of syllables in a randomly-generated word are, in this model, drawn
from a poisson distribution with a mode (or lambda). This mode defaults to 3.
The draw is adjusted to ensure no words with 0 syllables are generated.

PNULL_CONSONANTS
----------------

Within a specific syllable, when drawing a consonant-like sequence of
characters, there is a probability that it will be null or empty. This
probability is defined by a uniform draw against a fixed value--in this case,
0.3 (the value of the module-level variable *PNULL_CONSONANTS*).

In other words, there is a 30% chance that a syllable will not have a
consonant-like sequence of characters at the beginning. There is also a 30%
change that a syllable will not have a consonant-like sequence of characters at
the end. These draws are made independently.

Server Parameters
-----------------

There are also several server-specific parameters unrelated to the underlying
phonetic model. These can be customized by defining environmental variables
with the corresponding names.

* *SERVER_HOST* defines the host on which the WSGI server will listen (defaults to "0.0.0.0")

* *SERVER_PORT* defines the port on which the WSGI server will listen (defaults to 8000)
