
Note: Make sure you have the .env before you run the program
change the user details in the .env file

Start individual docker-compose file for to test it locally
and view the swagger docs <system ip>:<port>/docs

for example :
    http://192.168.68.109:8004/docs

Please update the .env file necessary fields

## Start the docker container
`if running first time`
- docker-compose up --build

`else`
- docker-compose up -d

### Access the Server
- Access the API docs at `localsystemIP:8001/docs`
- Access the API docs at `localsystemIP:8002/docs`
- Access the API docs at `localsystemIP:8003/docs`
- Access the API docs at `localsystemIP:8004/docs`
- Access the API docs at `localsystemIP:8005/docs`
