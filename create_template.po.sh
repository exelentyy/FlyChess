#!/bin/sh

xgettext --package-name=flychess -L Glade -o lang/flychess.pot glade/*.glade
xgettext --package-name=flychess -L Python -j -o lang/flychess.pot lib/flychess/Main.py lib/flychess/*/*.py lib/flychess/*/*/*.py

sed -i '/#, fuzzy/d' lang/flychess.pot

line=""Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n""
sed -i "/${line}/ s/^/# /" lang/flychess.pot
