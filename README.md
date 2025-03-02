# s n a f u  - test cli 

## Getting Started

1. Install and set up **twitch-cli** as described in the [Twitch Docs](https://dev.twitch.tv/docs/cli/).
you have to finish until u generated a token! 
2. Run:  
   ```sh
   twitch mock-api generate
   ```
3. Copy the credentials u generated into a `.env` file (example: `.env_example`)
4. Run:  
   ```sh
   twitch mock-api start
   ```
   you can change host/port 
   ```sh
   twitch event websocket start -p 8081
   ```

5. Run:  
   ```sh
   twitch event websocket start
   ```
   on unix u have to change port either on mock-server or websocket 
   ```sh
   twitch event websocket start -p 8081
   ```
6. check mock-server/websocket urls in `.env` file (example: `.env_example`) (u don't have to change them if u did the [Twitch Docs](https://dev.twitch.tv/docs/cli/) tutorial without changing ports..)

7. Run:  
   ```sh
   python test.py
   ```
8. copy the command printed by test.py into a console to trigger an event manually
