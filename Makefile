AR:=ar
CC:=gcc
SRCDIR:=src
DEMDIR:=main
OBJDIR:=build
INCDIR:=include
BINDIR:=bin
LIBDIR:=$(BINDIR)

INCS:=$(wildcard $(SRCDIR)/*.h)
OBJS:=$(subst $(SRCDIR)/,$(OBJDIR)/,$(patsubst %.c,%.o,$(wildcard $(SRCDIR)/*.c)))
DEMO_OBJS=$(OBJDIR)/mt19937ar.o $(OBJDIR)/parameters.o $(OBJDIR)/readline.o

CFLAGS:=-std=gnu99 -Wall -pedantic -march=native -O2 -g
IFLAGS:=-I$(INCDIR) -I/home/disk2/speed/walterjgsp/anaconda2/include/python2.7
LFLAGS:=-L$(LIBDIR) -lgges -lm  -lpython2.7

INC:=$(SRCDIR)/gges.h $(SRCDIR)/grammar.h $(SRCDIR)/cfggp.h $(SRCDIR)/ge.h \
	$(SRCDIR)/derivation.h $(SRCDIR)/individual.h $(SRCDIR)/mapping.h

LIB:=$(LIBDIR)/libgges.a
BIN:=$(BINDIR)/automaticML 

all: $(LIB) $(BIN)

lib: $(LIB)

$(LIBDIR)/libgges.a: $(OBJS) $(INCS)
	@echo creating library $@ from $^
	@mkdir -p $(BINDIR)
	@$(AR) -r $@ $(OBJS)
	@echo copying headers to $(INCDIR)
	@mkdir -p $(INCDIR)
	@cp $(INC) $(INCDIR)

$(BINDIR)/automaticML: $(DEMO_OBJS) $(OBJDIR)/automaticML.o $(LIB)
	@echo linking $@ from $^
	@$(CC) $(CFLAGS) $^ -o $@ $(LFLAGS)

$(OBJDIR)/%.o : $(SRCDIR)/%.c $(INCS)
	@echo compiling $< into $@
	@mkdir -p $(OBJDIR)
	@$(CC) $(CFLAGS) $(IFLAGS) -c $< -o $@

$(OBJDIR)/%.o : $(DEMDIR)/%.c $(wildcard $(DEMDIR)/*.h) $(INC)
	@echo compiling $< into $@
	@$(CC) $(CFLAGS) $(IFLAGS) -c $< -o $@

clean:
	@rm -rf $(OBJDIR) $(BINDIR)/automaticML

nuke: clean
	@rm -rf $(INCDIR) $(BINDIR) $(LIBDIR)

strip: all
	@echo running strip on $(BIN)
	@strip $(BIN)
