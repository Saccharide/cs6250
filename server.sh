#!/bin/bash

./out/Debug/quic_server --quic_response_cache_dir=/tmp/quic-data-backup/ --certificate_file=net/tools/quic/certs/out/leaf_cert.pem --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8 
