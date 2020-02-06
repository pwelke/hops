#!/bin/bash

sed 's/label=1/color="#e41a1c"/' < /dev/stdin | sed 's/label=2/color="#377eb8"/' | sed 's/label=3/color="#4daf4a"/' | sed 's/label=4/color="#984ea3"/' | sed 's/label=0/color="#ff7f00"/' > /dev/stdout