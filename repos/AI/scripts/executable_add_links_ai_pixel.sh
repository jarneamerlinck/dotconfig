#!/bin/bash
cd ~/repos/AI/ai-pixel-dreamer/
mkdir -p content/models
ln -s ~/repos/AI/models/dpt_large-midas-2f21e586.pt content/models/
ln -s ~/repos/AI/models/sd-v1-4.ckpt content/models/
mkdir -p pretrained
ln -s ~/repos/AI/models/AdaBins_nyu.pt pretrained/
