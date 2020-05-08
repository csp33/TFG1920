#!/bin/zsh
# Chatbot
docker build -t psychologist-bot chatbot
docker build -t mongo-populator mongo-populator
docker build -t nginx nginx

# Web interface
docker build -t web_interface web_interface