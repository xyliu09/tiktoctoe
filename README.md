1. Project Name

    TicTacToe-Backend

2. Project Description

    It's a restful web-service that allows customers to play the game of Tic-Tac-Toe.This REST API should allow players to create games, post moves, query moves and get the state of any game. The size of each game is limited to 3*3. 

3. How to Install and Run the Project
    Go to the tictoctoe project top level directory and do the following,
    
    3.1. Install virtualenv

        #On MacOS
        1. Open the terminal.
        2. Install virtualenv on Mac using pip:
            sudo python3 -m pip install virtualenv

        #On Windows
        1. Open the command line with administrator privileges.
        2. Use pip to install virtualenv on Windows:

            py -3 -m pip install virtualenv

    3.2 Activate the venv

        # macOS
        python3 -m venv .venv
        source .venv/bin/activate

        # Windows
        py -3 -m venv .venv
        .venv\scripts\activate

    3.3 Install packages
        pip install Flask
        pip install pytest

    3.4 Select python interpreter in the IDE

    3.5 Open the src/app/service.py, run ctrl + F5

4. How to use the project

    There are two ways to use the backend.

    4.1 Directly send http request to the service
    4.2 Build a front end on top of it, and integrate with our backend

5. Tests

    5.1 Local test

        Go to the tictoctoe/src/app directory, run service.py(ctrl + F5 in Windows), and use postman to send http request to each endpoint.

    5.2 Unit tests

        Go to the tictoctoe project top level directory, run "py.test" under the virtual env 

6. How does the service scale?

   We use a global variable as cache in this project for simplicity. We can use Redis for caching or migrate to using Flask-Caching, and use Flask-SQLAlchemy if we want to integrate the app with database for scalability.

   We can use a load balancer using K8s or API gateway to improve scalability.

   We should be careful of the RACE condition and use read/write LOCK. 

7. Future work

    7.1 Replace global variable with Redis or Flask-Caching

    7.2 Add the Swagger API doc. We don't have it now due to the time constraints.

    7.3 We use basic Flask here for simplicity. We should use Flask-RESTplus whenever possible, and it gives full Swagger support.

    7.4 Add more comprehensive tests