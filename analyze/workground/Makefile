STEP1_PATH = ""
STEP2_PATH = ""
STEP2_N_JOBS=4
STEP2_BATCH_SIZE=1000
STEP3_PATH = ""

run-all:
	pipenv run python lda

run-step1:
	pipenv run python -m lda --step_id=1 --path $(STEP1_PATH)

run-step2:
	pipenv run python -m lda --step_id=2 --path $(STEP2_PATH) --n_jobs $(STEP2_N_JOBS) --batch_size $(STEP2_BATCH_SIZE)

run-step3:
	pipenv run python -m lda --step_id=3 --path $(STEP3_PATH)
