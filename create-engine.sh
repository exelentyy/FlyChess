#!/bin/sh

cd lib

zip ../flychess-engine.pyz __main__.py flychess/__init__.py flychess/Players/__init__.py flychess/Players/flychess.py flychess/Players/flychessCECP.py flychess/Utils/lutils/*.py flychess/Utils/*.py flychess/System/__init__.py flychess/System/conf.py flychess/System/prefix.py flychess/System/Log.py flychess/Variants/*.py

cd ..
echo '#!/usr/bin/env python3' | cat - flychess-engine.pyz > flychess-engine
chmod +x flychess-engine
