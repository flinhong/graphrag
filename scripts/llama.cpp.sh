#!/usr/bin/sh

llama-server -m "C:\Users\honglin\.cache\lm-studio\models\nomic-ai\nomic-embed-text-v1.5-GGUF\nomic-embed-text-v1.5.Q4_K_M.gguf" -c 8192 -n -1 -t 7 --embeddings
