# turbo-octo-barnacle
grinder game test bed

## To play!!!

Run the following commands from repo root as needed:

1. Initialize the project after clone (only needed once)
    ```
    $ bin/init
    ```

2. Launch local instance of the game
    ```
    $ bin/playlocal
    ```

3. Launch web instance of the game utilizing the pygbag test server
    ```
    $ bin/playwebtest
    ```

4. Build artifacts for a hosted web instance of the game
    ```
    $ bin/buildweb
    ```

5. Build docker image (requires `bin/buildweb` be run first)
    ```
    $ bin/buildimage
    ```

6. Run docker image (requires `bin/buildimage` be run first)
    ```
    $ bin/runimage
    ```
