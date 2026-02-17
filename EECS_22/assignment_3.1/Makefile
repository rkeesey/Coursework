# compiler
CC = gcc

# compiler tags
CFLAGS = -Wall -std=c11 -g

# main targets
TGT_DEBUG = PhotoLabTest #debug mode executable
TGT_NORM = PhotoLab #regular mode executable

# debug conditions
debug: CFLAGS += -DDEBUG
debug: $(TGT_DEBUG)

# normal program
all: $(TGT_NORM)

$(TGT_NORM): FileIO.o DIPs.o Advanced.o PhotoLab.c
	$(CC) $(LFLAGS) FileIO.o DIPs.o Advanced.o PhotoLab.c -o $(TGT_NORM) -lm

$(TGT_DEBUG): FileIO.o DIPs.o Advanced.o PhotoLab.c
	$(CC) $(LFLAGS) -DDEBUG FileIO.o DIPs.o Advanced.o PhotoLab.c -o $(TGT_DEBUG) -lm

FileIO.o: FileIO.c FileIO.h Constants.h
	$(CC) $(CFLAGS) -c FileIO.c -o FileIO.o

DIPs.o: DIPs.c DIPs.h Constants.h
	$(CC) $(CFLAGS) -c DIPs.c -o DIPs.o

Advanced.o: Advanced.c Advanced.h Constants.h
		$(CC) $(CFLAGS) -c Advanced.c -o Advanced.o

clean:
	rm *.o $(PhotoLab) $(PhotoLabTest)

