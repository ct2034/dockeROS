#/bin/bash
docker run --name unsave_registry \
  -d \
  -v registry:/var/lib/registry \
  -p 5000:5000 \
  --restart=always \
  unsave_registry
