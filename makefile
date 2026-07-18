.DEFAULT_GOAL=listen

.venv/bin/python:
	python -m venv .venv

.venv/bin/pip: .venv/bin/python

.markers/requirements: requirements.txt
	.venv/bin/pip install -r requirements.txt
	mkdir -p .markers
	touch .markers/requirements

.envrc: example.envrc
	echo -e "\n# \`example.envrc\` has been updated, make the" >> .envrc
	echo -e "# changes required to your local .envrc.\n" >> .envrc
	cat example.envrc >> .envrc
	$${EDITOR:-vi} .envrc
	direnv allow

.markers/state:
	mkdir -p .state/who-up
	touch .markers/state

.PHONY: listen
listen: .venv/bin/python .markers/requirements .envrc .markers/state
	direnv exec .venv/bin/fastapi dev -e listen_for_signups:app --port 5802

.PHONY: start-shuffle
start-shuffle: .venv/bin/python .markers/requirements .envrc .markers/state
	direnv exec .venv/bin/python start_shuffle.py

.PHONY: finalise-shuffle
finalise-shuffle: .venv/bin/python .markers/requirements .envrc .markers/state
	direnv exec .venv/bin/python finalise_shuffle.py

lock.txt: .venv/bin/pip .markers/requirements requirements.txt
	.venv/bin/pip freeze > lock.txt

.PHONY: clean
clean:
	rm -rf .venv
	rm -rf .markers
	rm -rf .state

.PHONY: nuke
nuke: clean
	rm -f .envrc
