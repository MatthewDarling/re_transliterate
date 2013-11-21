Transliteration is the conversion of text from one orthography to
another, or if you're a linguist, from a phonetic orthography to 
transcription. I wrote this module to convert the orthography of an
indigenuous Mexican language into IPA: their orthography was based
on Spanish, so there weren't any confusing irregularities like in
English.

re_transliterate supports Unicode, though there might be corner cases
for particular languages. If that's the case, let me know, and I'll 
look into using the regex module from PyPI rather than the built-in re
module.

Unlike the transliterate package on PyPI, re_transliterate allows for 
mapping between arbitrary strings: one (or more) letters can correspond
to one (or more) letters. Since it's based on regular expressions, you
can also define language-specific character classes, like a set of
vowels. This is extremely useful for handling diacritics and other
suprasegmental features.

How does it work?
-----------------

re_transliterate relies on Python dictionaries - mappings of x:y. These
mappings should be written as regular expressions, which you may 
already be familiar with. If not, find a computer science undergrad and
make them write your mappings :)

In simple cases, you can simply use normal strings (prefaced by 'u' for
Unicode in Python 2):

    >>> consonant_map = {u"ch":u"č", u"x’":u"š’"}
    >>> word_replace(consonant_map, u"ch")
    č

With that mapping, occurrences of "ch" will be turned into 'č' and 
ejectives written with 'x' will instead use 'š'.

The power of regular expressions
--------------------------------

In more complicated cases, allowing regular expressions makes life
much simpler. We can use character classes to reduce repetition, and 
use backslashes to do fancy things. If your string contains a 
backslash, preface it with 'r' as well as 'u'. An example of both:

    >>> VOWELS = u"([aeiouáéíóú])"
    >>> long_vowels = {VOWELS + u":":ur"\g<1>ː"}
    >>> word_replace(long_vowels, u"a:'")
    aː

With this mapping, vowels followed by a colon character (':') will be
changed to use the IPA symbol for length ('ː'). Here, square brackets []
indicate a "character class": these characters will be treated in the 
same way, such that the string "a:" will be matched just like "i:" or 
"ú:".

Then, the parentheses () indicate a "group" in the regular expression:
this allows us to reference what it is that the pattern matched - 
that's what the \g<1> does, referring to "group 1". If the pattern were
to match "a:", it would insert "aː". This is the primary benefit of
using regular expressions: we don't have to specify that "a:" turns
into "aː", and that "e:" turns into "eː", etc.

Complicated mappings
--------------------

In the previous example, did you see that I used addition inside the
mapping? This allows useful patterns and special Unicode sequences to
be saved globally and reused elsewhere. In my own work, I defined the 
above character class of vowels, and the Unicode sequence for the "tilde
below letter" diacritic:

    >>> LARYNGEAL = ur"u\0330"

This allowed me to write mappings like this, where the ' character
represents laryngealization and may occur before/after a marker for
length:

    >>> long_laryngealized = {VOWELS + u":'|':":
                              ur"\g<1>" + LARYNGEAL + u"ː"}

This converts any vowel, followed by either (marked by '|') ":'" or
"':", into the vowel + laryngealization diacritic + length marker.

Applying your mappings
----------------------

Once you've created all your mappings, you can then either apply them
one at a time to a word (word_replace) or list of words
(word_list_replace). As you develop your conversion code, you should
use these functions first, to make sure everything is working correctly.

Generally, you'll want to have multiple mappings, because some
conversions will be sensitive to ordering. For my work, I created three
mappings: trigraphs (sequences of three characters), bigraphs, and 
monographs. I then applied each of those in order, using the two
transliterate functions. Example:

    >>> re_trigraphs = {u"lh’":u"ɬ’",
                        VOWELS + u":'|':":ur"\g<1>" + LARYNGEAL + u"ː"}
    >>> re_bigraphs = {u"ch":u"č", u"lh":u"ɬ", u"nh":u"ŋʔ",
                       u"tz":u"c", u"uj":u"ʍ",
                       u"s’":u"s’", u"x’":u"š’",
                       VOWELS + u":":ur"\g<1>ː",
                       VOWELS + u"'":ur"\g<1>" + LARYNGEAL}
    >>> re_monographs = {u"h":u"ʔ", u"r":u"ɾ", u"x":u"š"}
    >>> order = [re_trigraphs, re_bigraphs, re_monographs]
    >>> transliterate(order, u"a:ma'ha:'pi'tzín")
    aːma̰ʔa̰ːpḭcín

This way, the conversion for "lh":"ɬ" won't interrupt the conversion of
"lh’":u"ɬ’". Alternatively, I suppose you could use an OrderedDict with
the word_replace/word_list_replace functions, but I personally like it
this way.

Conclusion
----------

If you're writing your code in an interactive environment such as IPython,
note that if you change the contents of a dictionary, it will not be
updated inside any lists you may have created. I learned this the hard way,
when my code didn't work until I redefined the order list used above. If you
see any weird bugs, that might be the cause.

Other than that, if you have any other questions/issues with the module,
shoot me an e-mail; especially if you run into any issues with Unicode
support or bugs specific to Python 3/PyPy/another interpreter.