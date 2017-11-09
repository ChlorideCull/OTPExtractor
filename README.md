# OTPExtractor

Extract OTP keys from a Google Authenticator database and generate URIs for them, and optionally QR codes. Should go
without saying that those should still be kept secret.

## Usage

Run `OTPExtractor.py`, passing the path to the database (`databases`) as an argument, optionally adding `--qr` to
generate SVGs containing QR codes in the current working directory.

## Requirements

Some version of Python 3, any will probably do, and [qrcode](https://pypi.python.org/pypi/qrcode) from PyPI.
I tested it with Python 3.6 and qrcode 5.3, so that will work at least.