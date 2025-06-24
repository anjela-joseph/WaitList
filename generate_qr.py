import qrcode

# Change this to your deployed domain once live
url = "https://declutterminds-waitlist.onrender.com/waitlist/"  # or https://yourdomain.com/waitlist/

qr = qrcode.make(url)
qr.save("waitlist_qr.png")

print("QR code saved as waitlist_qr.png")
