import io
from ftplib import FTP

with FTP('localhost') as ftp:
    print(ftp.login('ftp', 'password'))
    # print(ftp.retrlines('LIST'))
    print(ftp.cwd('ftp/spp/sources'))
    print(ftp.retrlines('LIST'))
    # ftp.cwd('1')
    # ftp.retrbinary("RETR " + 'test.py', open('1.txt', 'wb').write)

    d = b'PNG?> test document PNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test document'
    ftp.storbinary("STOR " + "png.py", io.BytesIO(d), 1024)
    print(ftp.pwd())
