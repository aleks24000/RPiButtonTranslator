from RPiFunctions import start, stop_rec



if __name__ == '__main__':
    print("1")
    audiof = start( True )
    stop_rec(True, audiof)