#!/bin/bash

pip install -U ckiptagger[tf,gdown]
pip install -r requirment.txt
python download_ckipmodel.py
mv data/ CKIPMODEL/
