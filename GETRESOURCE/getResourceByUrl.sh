#!/bin/bash

# A simple script for fetching a resource.  No auth required.

#curl http://staging.oercommons.org/api/getResource?url=https://open.umich.edu/education/si/si680-winter2008
curl http://staging.oercommons.org/api/getResource?url=$1
