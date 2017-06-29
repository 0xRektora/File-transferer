import argparse
import socket
import hashlib
import os
import time
def client(_ip, _port, chunk, _checksum, *files):
    host = _ip
    port = _port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    server.send(str(chunk).encode("utf8"))
    server.recv(1024)

    for i in files:
        timestart = time.clock()
        if not _checksum:
            server.send(str(checksum(i, chunk)).encode("utf8"))
        else:
            server.send("nochecksum".encode("utf8"))
        temp = ""
        cursor = 0
        myfile = os.stat(i)
        file_size = myfile.st_size
        with open(i, "rb") as fichier:

            while True:
                fichier.seek(cursor)
                temp = fichier.read(chunk)
                if temp == b"":
                    break
                cursor += chunk
                percentage = (fichier.tell() / file_size)*100
                print("\r[+]Sending data {}%".format(percentage), flush=True, end="")
                server.send(temp)
    timefinished = time.clock()
    time_elapsed = timefinished - timestart
    print("\n[+]Sending finished in ", time_elapsed, "sec")
    server.close()


def checksum(filename, _chunk):
    print("[+]Creating checksum")
    filestat = os.stat(filename)
    file_size = filestat.st_size
    print("[+]File size :", file_size/1000000,"Mb")
    percentage = 0
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as myfile:
        for chunk in iter(lambda: myfile.read(_chunk), b""):
            percentage = (myfile.tell() / file_size)*100
            print(":\r[+]Percentage:{}%".format(percentage), flush=True, end="", sep=' ')
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def Main():
    parser = argparse.ArgumentParser(description="A simple client server")
    parser.add_argument("dest_IP", help="Destination IP", type=str)
    parser.add_argument("dest_PORT", help="Destination Port", type=int)
    parser.add_argument("-f", "--file", help="Files to send", type=str,
                        action="append")
    parser.add_argument("-ps", "--parse_speed",
                        help="define the chunk of memory to send in bytes",
                        type=int, default=20971520)
    parser.add_argument("-nc", "--nochecksum", help="Deactivate the checksum step", action="store_const", default=False, const=True)

    args = parser.parse_args()
    client(args.dest_IP, args.dest_PORT, args.parse_speed, args.nochecksum, * args.file)


if __name__ == "__main__":
    Main()
