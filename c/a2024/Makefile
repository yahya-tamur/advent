CC=clang
CFLAGS= -Ofast

all: $(patsubst %.c,%,$(wildcard *.c))

% : %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $$(basename -s .c *.c)
