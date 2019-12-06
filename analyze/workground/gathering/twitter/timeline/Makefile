#!make
include ../../../../Makefile

include .env
export

SCREEN_NAME=TwitterNewsJP

run-step1:
	$(PIPENV_PIPFILE) pipenv run python . step1 --screen_name=$(SCREEN_NAME)
