#!/bin/bash
if [[ -z $1  ]]; then
    echo "Need to specify website"
    exit 1
fi
./out/Debug/quic_client --host=127.0.0.1 --disable_certificate_verification --port=6121 https://www.$1/
