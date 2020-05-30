#include <elegoo.h>

#ifndef REMOTEINPUT
#define REMOTEINPUT

char process_remote_input(uint64_t input)
{
    switch (input)
    {
    case KEY_POWER:
        return 'P';
    case KEY_PAUSE:
        return '=';
    case KEY_STOP:
        return 'S';
    case KEY_VOL_UP:
        return 'A';
    case KEY_VOL_DOWN:
        return 'V';
    case KEY_0:
        return '0';
    case KEY_1:
        return '1';
    case KEY_2:
        return '2';
    case KEY_3:
        return '3';
    case KEY_4:
        return '4';
    case KEY_5:
        return '5';
    case KEY_6:
        return '6';
    case KEY_7:
        return '7';
    case KEY_8:
        return '8';
    case KEY_9:
        return '9';
    default:
        return (char)0;
    }
}

#endif