#!/bin/bash

# A simple script for fetching a resource.  No auth required.  Returns 
# a JSON-encoded result set.

# curl http://www.oercommons.org/api/getResource?id=6431
curl http://www.oercommons.org/api/getResource?id=$1
