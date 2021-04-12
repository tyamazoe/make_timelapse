#!/bin/bash
find ./ -name '*.jpg' | sort -n | awk 'BEGIN{ a=1 }{ printf "mv \"%s\" %04d.jpg\n", $0,a++}' | bash


