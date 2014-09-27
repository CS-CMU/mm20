/*
** Part of the testclient for mechmania 20
**
** The purpose of this class is to handle the decision-making for each turn of the game
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include "ai_objects.c"

//Given name, set up initial message
char * get_initial_message(char * name){
    char * str = malloc(150);
    return strcpy(str, "{\"team\":\"test\", \"members\":[{\"name\":\"test1\", \"archetype\":\"Coder\"},{\"name\":\"test2\", \"archetype\":\"Architect\"},{\"name\":\"test3\", \"archetype\":\"Theorist\"}]}");
}

sent_turn_t * get_turn(received_turn_t * received_turn) {
    return NULL;
}