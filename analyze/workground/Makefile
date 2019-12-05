STEP1_PATH = ""
STEP2_PATH = ""
STEP2_N_JOBS=4
STEP2_BATCH_SIZE=1000
STEP3_PATH = ""
STEP3_TOPIC_ID = 20
STEP4_FONT_PATH = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"

run-all:
	pipenv run python lda

run-step1:
	pipenv run python -m lda --step_id=1 --path $(STEP1_PATH)

run-step2:
	pipenv run python -m lda --step_id=2 --path $(STEP2_PATH) --n_jobs $(STEP2_N_JOBS) --batch_size $(STEP2_BATCH_SIZE)

run-step3:
	pipenv run python -m lda --step_id=3 --path $(STEP3_PATH) --topic_id $(STEP3_TOPIC_ID)

run-step4:
	pipenv run python -m lda --step_id=4 --font_path $(STEP4_FONT_PATH)
