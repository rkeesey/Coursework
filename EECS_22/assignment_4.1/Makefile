# compiler
CC = gcc

# compiler tags
CFLAGS = -Wall -std=c11 -g

# main targets
TGT_DEBUG = PhotoLabTest #debug mode executable
TGT_NORM = PhotoLab #regular mode executable

# normal program
all: $(TGT_NORM) $(TGT_DEBUG)

# debug conditions
debug: CFLAGS += -DDEBUG
debug: $(TGT_DEBUG)

$(TGT_DEBUG): FileIO.o DIPs.o Image.o Advanced.o Test.o PhotoLab.c Constants.h
	$(CC) $(LFLAGS) -DDEBUG Test.o FileIO.o DIPs.o Advanced.o Image.o PhotoLab.c -o $(TGT_DEBUG) -lm

$(TGT_NORM): FileIO.o DIPs.o Image.o PhotoLab.c Constants.h Advanced.o Test.o
	$(CC) $(LFLAGS) FileIO.o DIPs.o Image.o Advanced.o Test.o PhotoLab.c -o $(TGT_NORM) -lm

Image.o: Image.c Image.h 
	$(CC) $(CFLAGS) -c Image.c -o Image.o

FileIO.o: FileIO.c FileIO.h Image.h Constants.h 
	$(CC) $(CFLAGS) -c FileIO.c -o FileIO.o

DIPs.o: DIPs.c DIPs.h Image.h Constants.h
	$(CC) $(CFLAGS) -c DIPs.c -o DIPs.o

Advanced.o: Advanced.c Advanced.h Image.h Constants.h 	
	$(CC) $(CFLAGS) -c Advanced.c -o Advanced.o

Test.o: Test.c Test.h
	$(CC) $(CFLAGS) -c Test.c -o Test.o

clean:
	rm *.o *.ppm $(TGT_NORM) $(TGE_DEBUG) 
	cp ~eecs22/public/watermark_template.ppm .
	cp ~eecs22/public/border.ppm
	cp ~eecs22/public/EngPlaza.ppm

