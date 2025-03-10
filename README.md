# s n a f u  - test cli 

## Getting Started

1. Install and set up **twitch-cli** as described in the [Twitch Docs](https://dev.twitch.tv/docs/cli/).
you have to finish until u generated a token!
In this step u also have to create a [twitch-app](https://dev.twitch.tv/console/apps/create) for use with the twitch-cli. U have to set the OAuth Redirection URI to http://localhost:3000

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
   twitch mock-api start -p 8081
   ```

5. Run:  
   ```sh
   twitch event websocket start
   ```
   on unix u need different ports for websocket and mock-api
   ```sh
   twitch event websocket start -p 8081
   ```
6. check mock-server/websocket urls in `.env` file (example: `.env_example`) (u don't have to change them if u did the [Twitch Docs](https://dev.twitch.tv/docs/cli/) tutorial without changing ports.. hint: BASE is for mock-api-server and CONNECTION_URL and SUBSCRIPTION_URL for twitch-websocket)

7. Run:  
   ```sh
   python twitch-mocking.py
   ```
   or test it live on twitch with real credentials
   ```sh
   python live.py
   ```
8. copy the command printed by test.py into a console to trigger an event manually


if u use production, u currently have to change oauth url (twitch-dev-application-settings) to localhost:17xxx