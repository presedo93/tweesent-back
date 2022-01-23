# TweeSent Backend
Tweesent backend. This repo uses fastAPI as the web framework. Tweepy to request from Twitter all the needed data and ONNX to do the inference.

## fastAPI
Basically, the backend works with two types of requests. With the HTTP request, the user can ask for a certain amount of tweets inputing a text of an username (starting by @).

It also supports WebSockets connections, so the user can ask for a certain topic and have a live stream of tweets related with its predictions.

## ONNX
Models are trained using `pytorch-lightning` and results are exported to ONNX so they can be easily handled.

At startup, the backend will load the pertinent weights and will do the prediction in the tweets.

## Tweepy
Even the Twitter API v2 supports a maximum of 100 tweets per request, the backend can continue where it left using a token. So the first time the user asks for some tweets the backend will answer with the pertinent toker to continue the search later on.

## Docker
Best way to start the repo is using... Docker!! There is an awesome `Dockerfile` (pending to be improved) to start easily the backend.

## Pre commits hooks

Once downloaded the repo, and installed the needed packages in `requirements.txt`... it is desirable to install the git hooks for this repo!

    pre-commit install

This will install git hooks such as `black`, `flake8` or `mypy`.

## To-do

- [ ] Improve Dockerfile so it supports multi-stage builds.
- [ ] Support some way to fetch a model in case there is no one in the weights folder at startup.
