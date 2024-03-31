CC = clang
CFLAGS = -std=c99 -Wall -pedantic

all: phylib.o libphylib.so phylib_wrap.o _phylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o -fpic

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib_wrap.c phylib.py: phylib.i phylib.h
	swig -python -o phylib_wrap.c phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.9/ -fPIC -o phylib_wrap.o 

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) -shared phylib_wrap.o -L. -L/usr/lib/python3.9 -lpython3.9 -lphylib -dynamiclib -o _phylib.so

clean:
	rm -f *.o *.so phylib_wrap.c phylib.py _phylib.so libphylib.so *.svg *.db
