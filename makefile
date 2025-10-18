d ?= 60
epsilon_max ?= 0.09
rho ?= 1e-2

.PHONY: run_project clean

run_project:
	python3 server.py &
	python3 network.py &
	sleep 2
	python3 client.py --d $(d) --epsilon_max $(epsilon_max) --rho $(rho)
	@make clean

clean:
	@pkill -f server.py || true
	@pkill -f network.py || true
