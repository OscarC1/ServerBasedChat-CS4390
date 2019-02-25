# # Build system
#
# # Authors:
# - Seth Giovanetti

DOC_SRC=$(shell find Doc/ -name "*.md")

all: documentation client server


clean:


documentation: $(DOC_SRC:%.md=%.html)

%.html: %.md
	@echo "You will need to build '$@' manually using Typora."

client:

server:

