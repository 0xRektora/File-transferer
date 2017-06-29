import socket
import argparse
import os
import sys
import time
import hashlib
import threading
parser = argparse.ArgumentParser(description="File transfer server program")
parser.add_argument("filename", help="the name of the file to save and the " +
                    "format")
args = parser.parse_args()
if os.path.exists(args.filename):
    print("[-]File name already exist, [D]elete or [C]hange name.")
    uChoice = str(input(""))
    if uChoice == "D" or uChoice == "d":
        os.remove(args.filename)
    elif uChoice == "C" or uChoice == "c":
        args.filename = str(input("[+]Enter a new name: "))
    else:
        print("[-_-] The fuck you're saying ?")
        exit()


def checksum(filename, _chunk):
    print("[+]Creating checksum")
    filestat = os.stat(filename)
    file_size = filestat.st_size
    print("[+]File size :", file_size/1000000, "Mb")
    percentage = 0
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as myfile:
        for chunk in iter(lambda: myfile.read(_chunk), b""):
            percentage = (myfile.tell() / file_size)*100
            print(":\r[+]Percentage:{}%".format(percentage), flush=True, end="", sep=' ')
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def Main():
    print("[+]Server opened by default on port 9999")
    host = ""
    port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print("[+]Waiting for connection\n")
    conn, addr = server.accept()
    print("[+]Got connection from", addr)
    timestart = time.clock()
    chunk = conn.recv(1024)
    conn.send(b"1")
    chunk = int(chunk.decode("utf8"))
    clientmd5hash = conn.recv(1024)
    clientmd5hash = clientmd5hash.decode("utf8")
    check = True
    if clientmd5hash == "nochecksum":
        check = False
    with open(args.filename, "ab") as filetowrite:
        filetowrite.write(b"")
    data_size = 0
    while True:
        data = conn.recv(chunk)
        data_size += sys.getsizeof(data)
        print("\r[+]Writing data: {} Mb".format(data_size/1000000), flush=True, end='')
        with open(args.filename, "ab") as fichier:
            fichier.write(data)

        if not data:
            print("\n[-]Connection lost")
            break
    if check:
        md5hash = checksum(args.filename, chunk)
        print("\n[+]Client hash: ", clientmd5hash)
        print("[+]Recvd file hash: ", md5hash)
        if md5hash == clientmd5hash:
            print("[+]Checksum true")
        else:
            print("[-]File may be corrupted")
    timefinished = time.clock()
    time_elapsed = timefinished - timestart
    print("\n[+]Sending finished in ", time_elapsed, "sec")
    print("\n[+]Connection closed")
    server.close()


if __name__ == "__main__":
    Main()
