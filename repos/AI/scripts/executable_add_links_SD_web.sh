#!/bin/bash
cd ~/repos/AI/stable-diffusion-webui/
ln -s ~/repos/AI/models/GFPGANv1.3.pth .
ln -s ~/repos/AI/models/sd-v1-4.ckpt models/
ln -s ~/repos/AI/models/sd-v1-4-full-ema.ckpt models/
ln -s ~/repos/AI/scripts/sd_scripts/* scripts/


# start adding stuff for extra scripts

cd /tmp
mkdir SD_setup
gh repo clone ThereforeGames/txt2mask
cd txt2mask
mv scripts/txt2mask.py ~/repos/AI/stable-diffusion-webui/scripts/
cp -r repositories/clipseg ~/repos/AI/stable-diffusion-webui/repositories/
rm -rf /tmp/SD_setup


