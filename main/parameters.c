#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gges.h"
#include "readline.h"

static void parse_param(char *line, char **key, char **value)
{
    *key = line;

    while (*line != '=') line++;
    *line = '\0';

    *value = line + 1;

    *key = trim(*key);
    *value = trim(*value);
}

void process_parameter(char *param, struct gges_parameters *params)
{
    char *line, *key, *value;

    line = malloc(strlen(param) + 1);
    strcpy(line, param);

    parse_param(line, &key, &value);

    if (strncmp(key, "pop_size", 8) == 0) {
        params->population_size = atoi(value);
    } else if (strncmp(key, "generations", 11) == 0) {
        params->generation_count = atoi(value);
    } else if (strncmp(key, "elitism", 7) == 0) {
        params->elitism_count = atoi(value);
    } else if (strncmp(key, "tourn_size", 10) == 0) {
        params->tournament_size = atoi(value);
    } else if (strncmp(key, "cache", 5) == 0) {
        params->cache_fitness = (value[0] == 'Y');
    } else if (strncmp(key, "crossover_rate", 14) == 0) {
        params->crossover_rate = atof(value);
    } else if (strncmp(key, "mutation_rate", 13) == 0) {
        params->mutation_rate = atof(value);
    } else if (strncmp(key, "init_min_depth", 14) == 0) {
        params->init_min_depth = atoi(value);
    } else if (strncmp(key, "init_max_depth", 14) == 0) {
        params->init_max_depth = atoi(value);
    } else if (strncmp(key, "init_codon_count", 16) == 0) {
        params->init_codon_count = atoi(value);
    } else if (strncmp(key, "max_mut_depth", 13) == 0) {
        params->maximum_mutation_depth = atoi(value);
    } else if (strncmp(key, "depth_limit", 11) == 0) {
        params->maximum_tree_depth = atoi(value);
    } else if (strncmp(key, "search_method", 13) == 0) {
        if (strncmp(value, "RANDOM", 6) == 0) {
            params->generation_method = RANDOM_SEARCH;
        } else if (strncmp(value, "GENERATIONAL", 12) == 0) {
            params->generation_method = GENERATIONAL;
        } else if (strncmp(value, "STEADY_STATE", 12) == 0) {
            params->generation_method = STEADY_STATE;
        } else {
            fprintf(stderr, "ERROR: Unknown value for parameter search_method: %s\n", value);
            exit(EXIT_FAILURE);
        }
    } else if (strncmp(key, "representation", 14) == 0) {
        if (strncmp(value, "CFG-GP", 6) == 0) {
            params->model = CONTEXT_FREE_GP;
        } else if (strncmp(value, "GE", 2) == 0) {
            params->model = GRAMMATICAL_EVOLUTION;
        } else {
            fprintf(stderr, "ERROR: Unknown value for parameter search_method: %s\n", value);
            exit(EXIT_FAILURE);
        }
    } else if (strncmp(key, "sensible_init_tail", 18) == 0) {
        params->sensible_init_tail_length = atof(value);
    } else if (strncmp(key, "sensible_init", 13) == 0) {
        params->sensible_initialisation = (value[0] == 'Y');
    /*} else if (strncmp(key, "dataTrainingDir", 12) == 0) {
       params->dataTraining = malloc(strlen(value) + 1);
       strcpy(params->dataTraining, value);   
    } else if (strncmp(key, "dataTestDir", 8) == 0) {
        params->dataTest  = malloc(strlen(value) + 1);
        strcpy(params->dataTest, value); 
    */
    } else if (strncmp(key, "grammarDir", 10) == 0) {
        params->grammarDir  = malloc(strlen(value) + 1);
        strcpy(params->grammarDir, value);
    } else if (strncmp(key, "internalCV", 10) == 0) {
        params->internalCV = atoi(value);         
    }else {
        fprintf(stderr, "WARNING: Unknown parameter: %s\n", key);
    }

    free(line);
}

void parse_parameters(char *params_file, struct gges_parameters *params)
{
    FILE *input;
    char *buffer, *line;
    size_t bufsz;

    input = fopen(params_file, "r");
    buffer = line = NULL;
    bufsz = 0;

    line = next_line(&buffer, &bufsz, input);
    while (!feof(input)) {
        if (strlen(line) > 0) {
            process_parameter(line, params);
        }
        line = next_line(&buffer, &bufsz, input);
    }
    fclose(input);
    free(buffer);
}
