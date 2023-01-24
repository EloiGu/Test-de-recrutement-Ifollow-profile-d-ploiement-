#include <iostream>
#include <mosquitto.h>
#include <cstring>
#include <ncurses.h>
using namespace std;


const char* HOST = "localhost";
const int PORT = 1883;
const char* TOPIC = "speed_from_keyboard_topic";

int main() {
    // Initialize the Mosquitto library
    mosquitto_lib_init();

    // Create a new Mosquitto client instance
    struct mosquitto* client = mosquitto_new("publisher", true, nullptr);

    // Connect the client to the MQTT broker
    mosquitto_connect(client, HOST, PORT, 60);

    // Wait for the connection to be established
    int result = mosquitto_loop_start(client);
    if (result != MOSQ_ERR_SUCCESS) {
        std::cerr << "Error: Unable to connect to the MQTT broker" << std::endl;
        return 1;
    }

  
    // Initialize ncurses
    initscr();

    // Disable line buffering and special keys
    cbreak();
    noecho();

    // Enable the keypad for non-character keys
    keypad(stdscr, TRUE);

    // Speed order
    float ahead = 0;
    float right = 0;

    printw("Use the directional arrows to influence the speed of the robot \n Press q  or ctlr+c to exit \n");
    
    // String initialization
    string message_ahead = "0";
    string message_right = "0";
    string finale_message;
    char separation = '/';

    // Wait for user input
    int ch = getch();
    
    while (ch != 'q') {     // Press q to STOP
        switch (ch) {
            case KEY_UP:
                printw(" Up arrow pressed  |");
                ahead = ahead + 0.1;
                message_ahead = to_string(ahead);
                break;
            case KEY_DOWN:
                printw(" Down arrow pressed  |");
                ahead = ahead - 0.1;
                message_ahead = to_string(ahead);
                break;
            case KEY_LEFT:
                printw(" Left arrow pressed  |");
                right = right + 0.1;
                message_right = to_string(right);
                break;
            case KEY_RIGHT:
                printw(" Right arrow pressed  |");
                right = right - 0.1;
                message_right = to_string(right);         
                break;
            default:
                break;
        }

        // combination of two direction messages in one
        finale_message = message_ahead + separation + message_right;
        const char* MESSAGE = finale_message.c_str();
        mosquitto_publish(client, nullptr, TOPIC, strlen(MESSAGE), MESSAGE, 1, false);
        //printw("Message published" );
        ch = getch();
    }
    endwin();



    // Disconnect the client from the broker
    mosquitto_disconnect(client);

    // Cleanup the Mosquitto library
    mosquitto_lib_cleanup();
}
