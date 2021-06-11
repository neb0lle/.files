#!/bin/sh
nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = $1 }"
echo FFC:$1
