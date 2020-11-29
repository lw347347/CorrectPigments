#!/bin/bash
cd /home/landonw347/CorrectPigments
daphne -b 0.0.0.0 -p 80 WebSockets.asgi:application
