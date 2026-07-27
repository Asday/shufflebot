.DEFAULT_GOAL=listen

currentDir=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))

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
	mkdir -p .markers
	touch .markers/state

.markers/config:
	mkdir -p .config
	mkdir -p .markers
	touch .markers/config

.PHONY: listen
listen: .venv/bin/python
listen: .markers/requirements
listen: .envrc
listen: .markers/state
listen: .markers/config
	direnv exec .venv/bin/fastapi dev -e listen_for_signups:app --port 5802

.PHONY: start-shuffle
start-shuffle: .venv/bin/python
start-shuffle: .markers/requirements
start-shuffle: .envrc
start-shuffle: .markers/state
start-shuffle: .markers/config
	direnv exec .venv/bin/python start_shuffle.py

.PHONY: finalise-shuffle
finalise-shuffle: .venv/bin/python
finalise-shuffle: .markers/requirements
finalise-shuffle: .envrc
finalise-shuffle: .markers/state
finalise-shuffle: .markers/config
	direnv exec .venv/bin/python finalise_shuffle.py

lock.txt: .venv/bin/pip .markers/requirements requirements.txt
	.venv/bin/pip freeze > lock.txt

systemd/shufflebot@listen_for_signups.service: systemd/shufflebot@listen_for_signups.service.example
	cp \
		systemd/shufflebot@listen_for_signups.service.example \
		systemd/shufflebot@listen_for_signups.service
	sed \
		-i \
		"s#/path/to/project/root/#${currentDir}#g" \
		systemd/shufflebot@listen_for_signups.service
	sed \
		-i \
		-E "s#[^/]+/\.\.[/$$]##g" \
		systemd/shufflebot@listen_for_signups.service

systemd/shufflebot@start_shuffle.service: systemd/shufflebot@start_shuffle.service.example
	cp \
		systemd/shufflebot@start_shuffle.service.example \
		systemd/shufflebot@start_shuffle.service
	sed \
		-i \
		"s#/path/to/project/root/#${currentDir}#g" \
		systemd/shufflebot@start_shuffle.service
	sed \
		-i \
		-E "s#[^/]+/\.\.[/$$]##g" \
		systemd/shufflebot@start_shuffle.service

systemd/shufflebot@finalise_shuffle.service: systemd/shufflebot@finalise_shuffle.service.example
	cp \
		systemd/shufflebot@finalise_shuffle.service.example \
		systemd/shufflebot@finalise_shuffle.service
	sed \
		-i \
		"s#/path/to/project/root/#${currentDir}#g" \
		systemd/shufflebot@finalise_shuffle.service
	sed \
		-i \
		-E "s#[^/]+/\.\.[/$$]##g" \
		systemd/shufflebot@finalise_shuffle.service

.PHONY: systemd
systemd: systemd/shufflebot@listen_for_signups.service
systemd: systemd/shufflebot@start_shuffle.service
systemd: systemd/shufflebot@finalise_shuffle.service

../secrets/env: example.envrc
	sudo mkdir -p ../secrets
	sudo sh -c 'cat example.envrc >> ../secrets/env'
	sudo sed -i 's/export //g' ../secrets/env
	sudo sed -i '/^STATE_DIRECTORY/d' ../secrets/env
	sudo $${EDITOR:-vi} ../secrets/env

.markers/installed: systemd/shufflebot@start_shuffle.service
.markers/installed: systemd/shufflebot@finalise_shuffle.service
.markers/installed: systemd/shufflebot@listen_for_signups.service
.markers/installed: ../secrets/env
	rm -f .markers/uninstalled
	sudo systemctl enable ${currentDir}systemd/shufflebot@start_shuffle.service
	sudo systemctl enable ${currentDir}systemd/shufflebot@start_shuffle.timer
	sudo systemctl enable ${currentDir}systemd/shufflebot@finalise_shuffle.service
	sudo systemctl enable ${currentDir}systemd/shufflebot@finalise_shuffle.timer
	sudo systemctl enable ${currentDir}systemd/shufflebot@listen_for_signups.service
	sudo systemctl daemon-reload
	sudo systemctl start shufflebot@start_shuffle.timer
	sudo systemctl start shufflebot@finalise_shuffle.timer
	sudo systemctl start shufflebot@listen_for_signups
	mkdir -p .markers
	touch .markers/installed

.markers/uninstalled:
	rm -f .markers/installed
	sudo systemctl disable shufflebot@start_shuffle.timer
	sudo systemctl disable shufflebot@finalise_shuffle.timer
	sudo systemctl stop shufflebot@listen_for_signups.service
	sudo systemctl disable shufflebot@listen_for_signups.service
	mkdir -p .markers
	touch .markers/uninstalled

.PHONY: install
install: .venv/bin/python .markers/requirements .markers/installed

.PHONY: uninstall
uninstall: .markers/uninstalled

.PHONY: clean-systemd
clean-systemd:
	rm -rf systemd/shufflebot@finalise_shuffle.service
	rm -rf systemd/shufflebot@listen_for_signups.service
	rm -rf systemd/shufflebot@start_shuffle.service

.PHONY: clean
clean: clean-systemd
	rm -rf .venv
	rm -rf .markers
	rm -rf .state

.PHONY: clean-all
clean-all: clean
	rm -rf .config

.PHONY: nuke
nuke: clean
	rm -f .envrc
