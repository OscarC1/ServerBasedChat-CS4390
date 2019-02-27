# # Build system
#
# # Authors:
# - Seth Giovanetti

DOC_SRC=$(shell find Doc/ -name "*.md")
PY_SRC=$(shell find src/ -name "*.py")

all: prereqs client server documentation


clean:

prereqs: requirements.txt
	python3 -m pip install --user -r requirements.txt

requirements.txt: $(PY_SRC)
# 	pip freeze > requirements.txt

documentation: $(DOC_SRC:%.md=%.html)

%.html: %.md
	@echo "You will need to build '$@' manually using Typora."

client:

server:

