# s n a f u  - test cli 

## Getting Started

1. Install and set up **twitch-cli** as described in the [Twitch Docs](https://dev.twitch.tv/docs/cli/).
2. Run:  
   ```sh
   twitch mock-api generate
3. Copy the credentials u generated into a `.env` file (example: `.env_example`)
4. Run:  
   ```sh
   twitch mock-api start
5. Run:  
   ```sh
   twitch event websocket start
6. check websocket urls in `.env` file (example: `.env_example`) (u don't have to change them if u did the [Twitch Docs](https://dev.twitch.tv/docs/cli/) tutorial without changing ports..)
7. Run:  
   ```sh
   python test.py
8. copy the command printed by test.py into a console to trigger an event manually
