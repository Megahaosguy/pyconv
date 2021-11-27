#!/bin/bash
for i in *.jpg *.jpeg *.jfif *.png *.gif; do
    [ -f "$i" ] || continue
    echo "$i"
    pyconv $i
done
