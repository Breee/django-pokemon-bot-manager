#!/bin/sh

if [ -z "$(ls -A /volume)" ]; then
  cp -R /code/* /volume
else
   echo "Volume is not Empty. Please mount an empty volume."
fi
