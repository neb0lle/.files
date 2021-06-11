#!/bin/sh
curl http://ip-api.com/json/$1 | jq
