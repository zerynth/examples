# ZDM simple for on premise server example

This project provides an examples to connect Zerynth devices to a ZDM on premise server hosted on a custom domain.

The feature is supported starting by Zerynth3 SDK v3.0.16.

## Requirements

Here is a list of required elements for the firmware.

* The domain used to host the ZDM on premise services.
* The Certification Authority (CA) certificate in .pem format.

## Key ZDM agent configuration points

The required configuration for the ZDM Agent in the firmware are the following.

* ZMQTT server URL, built from domain name of the hosted server.
* Binary files upload URL, built from domain name of the hosted server.
* Custom SSL context with custom CA certificate.

See the comments into main.py for more details.
