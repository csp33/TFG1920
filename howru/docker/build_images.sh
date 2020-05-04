#!/bin/zsh
# Chatbot
docker build -t psychologist-bot chatbot
docker build -t mongo-populator mongo-populator

# Web interface