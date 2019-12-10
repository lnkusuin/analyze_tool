include ../../Makefile

include .env
export

run-all:
	@make run-prepare
	@make run-nlp
	@make run-learn

run-prepare:
	$(PIP_RUN) prepare --path $(STEP1_PATH) --type=json

run-nlp:
	$(PIP_RUN) nlp --path $(STEP2_PATH) --n_jobs $(STEP2_N_JOBS) --batch_size $(STEP2_BATCH_SIZE)

run-learn:
	$(PIP_RUN) learn --path $(STEP3_PATH) --font_path $(FONT_PATH)

#run-step4:
#	$(PIPENV_PIPFILE) pipenv run python . step4 --font_path $(STEP4_FONT_PATH)

run-classify:
	$(PIP_RUN) classify

run-relearn:
	$(PIP_RUN) relearn --font_path $(FONT_PATH)
