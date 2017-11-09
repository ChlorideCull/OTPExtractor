#!/usr/bin/python3
#
# OTPExtractor
# Copyright (c) Sebastian Johansson, 2017
# Licensed under the EUPL
#
import sqlite3
import argparse
import qrcode
import qrcode.image.svg


def open_db(path):
    newdb = sqlite3.connect(database=path)
    return newdb


def output_url(keytype, label, issuer, secret, counter=None):
    """

    :type counter: int
    :type secret: str
    :type keytype: str
    :type label: str
    :type issuer: str
    """
    if keytype not in ["totp", "hotp"]:
        raise AssertionError("Key type has to be TOTP or HOTP.")
    if keytype == "hotp" and counter is None:
        raise AssertionError("Key type is HOTP but no counter was provided")
    if keytype == "totp" and counter is not None:
        raise AssertionError("Key type is TOTP but counter was provided")
    if label is None:
        raise AssertionError("No label was provided, but is required.")
    if secret is None:
        raise AssertionError("No secret was provided, but is required. No point without one, really.")

    label = label.replace("%3A", ":")

    if issuer is None or issuer == "":
        if ":" not in label:
            raise AssertionError("No issuer was provided, and label did not contain issuer.")
        issuer = label.split(sep=':')[0]
    elif ":" not in label:
        label = issuer + ":" + label

    builturl = "otpauth://{}/{}?secret={}&issuer={}".format(keytype, label, secret, issuer)
    if counter is not None:
        builturl += "&counter={}".format(counter)
    return builturl, label, issuer


def make_qr(url, label):
    qrc = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathFillImage)
    fname = label.replace(":", "_"
                ).replace("@", "_"
                ).replace(".", "_")
    with open(fname + ".svg", mode="wb") as f:
        qrc.save(stream=f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('database', metavar='<Google Authenticator Database>',
                    help="Extracted database from data folder of Google Authenticator, file named \"databases\".")
    ap.add_argument('--qr', action="store_true",
                    help="Generate SVG QR codes for each OTP key to the current directory, instead of printing them.")
    args = ap.parse_args()
    db = open_db(args.database)

    cur = db.cursor()
    # noinspection SqlNoDataSourceInspection,SqlResolve
    cur.execute("SELECT email, secret, counter, type, issuer FROM accounts")
    for row in cur:
        keytype = ""
        if row[3] == 0:
            keytype = "totp"
        elif row.type == 1:
            keytype = "hotp"

        outurl, corrlabel, corrissuer = output_url(keytype, row[0], row[4], row[1], row[2] if keytype == "hotp" else None)
        if args.qr:
            make_qr(outurl, corrlabel)
        else:
            print(outurl)


if __name__ == "__main__":
    main()
