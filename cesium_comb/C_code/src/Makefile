CUDA_INSTALL_PATH ?= /opt/cuda-toolkit

# Directories
BINDIR = ../bin
OBJDIR = ./obj
# Compilers
NVCC       := $(CUDA_INSTALL_PATH)/bin/nvcc
CXX        := g++ -fPIC
CC         := gcc -fPIC
LINK       := g++ -fPIC


INCLUDES  += -I. -I$(CUDA_INSTALL_PATH)/include
NVINCLUDES  += -I. -I$(CUDA_INSTALL_PATH)/include/ -I/usr/share/cuda-sdk/C/common/inc
CFLAGS = -O3
NVFLAGS = -lcublas -L/usr/share/cuda-sdk/C/lib  --compiler-bindir=gcc -m64 --compiler-options '-O3 -fno-strict-aliasing'
NVFLAGS_SHARE = -shared -Xcompiler -fpic -lcublas -L/usr/share/cuda-sdk/C/lib --compiler-bindir=gcc -m64 --compiler-options '-O3 -fPIC'

all: cublasTest

cublasTest: main.o  libmatrixMul.so #matrixMul_gold.o
	$(NVCC) $(NVINCLUDES) $(NVFLAGS) -o $(BINDIR)/main $(OBJDIR)/main.o  ../src/obj/libmatrixMul.so 

main.o: main.c
	$(CXX) $(NVINCLUDES) $(CFLAGS) -o $(OBJDIR)/main.o -c main.c

libmatrixMul.so: matrixMul.cu
	$(NVCC) $(NVINCLUDES) $(NVFLAGS_SHARE) -o $(OBJDIR)/libmatrixMul.so matrixMul.cu

clean:  tidy
	rm $(BINDIR)/* $(OBJDIR)/*
tidy :
	$(VERBOSE)find . | egrep "#" | xargs rm -f
	$(VERBOSE)find . | egrep "\~" | xargs rm -f
