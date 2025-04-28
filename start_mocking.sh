source /home/snafu/src/5n4fu_live/venv/bin/activate

twitch mock-api start -p 5555 &
twitch event websocket start -p 5556 &

python3 /home/snafu/src/5n4fu_cli/twitch-mocking.py