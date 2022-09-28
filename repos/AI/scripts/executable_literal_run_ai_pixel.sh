#!/bin/bash
cd ~/repos/AI/ai-pixel-dreamer/
source ~/.conda/etc/profile.d/conda.sh
conda activate aidreamer

streamlit run scripts/webui_streamlit.py
