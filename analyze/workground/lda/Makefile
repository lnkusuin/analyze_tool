include ../../../Makefile

include .env
export

run-all:
	@make run-step1
	@make run-step2
	@make run-step3
	@make run-step4

run-step1:
	$(PIPENV_PIPFILE) pipenv run python . step1 --path $(STEP1_PATH) --type=json

run-step2:
	$(PIPENV_PIPFILE) pipenv run python . step2 --path $(STEP2_PATH) --n_jobs $(STEP2_N_JOBS) --batch_size $(STEP2_BATCH_SIZE)

run-step3:
	$(PIPENV_PIPFILE) OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES pipenv run python . step3 --path $(STEP3_PATH) --font_path $(FONT_PATH)

#run-step4:
#	$(PIPENV_PIPFILE) pipenv run python . step4 --font_path $(STEP4_FONT_PATH)
