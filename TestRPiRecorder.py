from RPiFunctions import start, stop_rec, upload_file



if __name__ == '__main__':

    audiof = start( True )
    stop_rec(True)
    upload_file()