#include <stdio.h>
#include <stdlib.h>

#include <math.h>

#include "gges.h"
#include "individual.h"

#include "alloc.h"

/* performs a simple comparison of two individuals to sort then in
 * descending order of fitness (i.e. individuals with greatest fitness
 * appear earlier in the sort). Valid (i.e., mapped) individuals
 * outrank invalid in this sort */
static int compare_individuals(const void *a, const void *b)
{
    double fa, fb;
    bool ma, mb;

    ma = (*(struct gges_individual * const *)a)->mapped;
    mb = (*(struct gges_individual * const *)b)->mapped;

    if (ma && mb) {
        /* if both were valid, then base comparison on fitness */
        fa = (*(struct gges_individual * const *)a)->fitness;
        fb = (*(struct gges_individual * const *)b)->fitness;

        if (fa > fb) {
            return -1;
        } else if (fa < fb) {
            return 1;
        } else {
            return 0;
        }
    } else if (ma) {
        return -1;
    } else if (mb) {
        return 1;
    } else {
        return 0;
    }
}

static struct gges_population *create_population(struct gges_parameters *params)
{
    struct gges_population *pop;

    pop = ALLOC(1, sizeof(struct gges_population), false);
    pop->members = ALLOC(params->population_size, sizeof(struct gges_individual *), false);

    pop->N = 0;
    while (pop->N < params->population_size) {
        pop->members[pop->N++] = gges_create_individual(params);
    }

    return pop;
}

static void check_depth_parameters(struct gges_parameters *params,
                                   struct gges_bnf_grammar *grammar)
{
    int min_depth;

    /* extract the depth of the smallest possible derivation tree from
     * the grammar's start non-terminal */
    if (grammar->start == NULL) {
        min_depth = grammar->non_terminals[0].min_depth;
    } else {
        min_depth = grammar->start->min_depth;
    }

    /* if the shortest derivation tree that can be produced from the
     * supplied grammar is taller than the supplied minimum depth,
     * then overwrite the parameter, otherwise use the supplied
     * parameter for minimum derivation tree depth */
    if (min_depth > params->init_min_depth) {
        /* if the user has supplied a value, then let them know that
         * their setting is invalid */
        if (params->init_min_depth > 0) {
            fprintf(stderr, "%s:%d - Warning! Minimum depth of grammar is "
                    "greater than the defined minimum derivation tree depth. "
                    "Setting minimum derivation tree depth to minimum depth "
                    "of grammar.\n",
                    __FILE__, __LINE__);
        }
        params->init_min_depth = min_depth;
    } else {
        min_depth = params->init_min_depth;
    }

    /* if the minimum tree depth that we wish to create is actually
     * larger than the supplied maximum depth, then overwrite the user
     * parameter and use the minimum depth */
    if (min_depth > params->init_max_depth) {
        fprintf(stderr, "%s:%d - Warning! Minimum derivation tree depth is "
                "greater than the defined maximum derivation tree depth. "
                "Setting maximum derivation tree depth to minimum depth of "
                "grammar.\n",
                __FILE__, __LINE__);

        params->init_max_depth = min_depth;
    }
}

static void initialise_population_rhh(struct gges_parameters *params,
                                      struct gges_bnf_grammar *grammar,
                                      struct gges_population *pop,
                                      GGES_EVAL evaluator,
                                      int current_generation,
                                      void *args)
{
    int i, min_depth, max_depth, depth_range;
    bool grow;

    check_depth_parameters(params, grammar);

    min_depth = params->init_min_depth;
    max_depth = params->init_max_depth;

    depth_range = 1 + max_depth - min_depth;
    grow = false;
    for (i = 0; i < pop->N; ++i) {
        /* decide between using grow and full modes of tree development */
        if ((i % depth_range) == 0) grow = !grow;

        /* work out the maximum tree depth for this individual */
        params->init_max_depth = min_depth + (i % depth_range);
        if (grow) {
            params->init_min_depth = min_depth;
        } else {
            params->init_min_depth = params->init_max_depth;
        }

        /* after all that, we finally perform the actual
         * initialisation of the individual */
        gges_init_individual(params, grammar, pop->members[i]);
    }



    /* Initialize the evaluation for each individual */
    for (i = 0; i < pop->N; ++i) {
        pop->members[i]->fitness = 0.0;
    }
    /*Evaluate the whole population */
    evaluator(params, current_generation, pop->members, pop->N, args);


    /* reset the user parameters to their pre-defined values, or to
     * the adjusted "sensible" values */
    params->init_min_depth = min_depth;
    params->init_max_depth = max_depth;
}

static void initialise_population_rnd(struct gges_parameters *params,
                                      struct gges_bnf_grammar *grammar,
                                      struct gges_population *pop,
                                      GGES_EVAL evaluator,
                                      int current_generation,
                                      void *args)
{
    int i;

    check_depth_parameters(params, grammar);

    for (i = 0; i < pop->N; ++i) {
        /* after all that, we finally perform the actual
         * initialisation of the individual */
        gges_init_individual(params, grammar, pop->members[i]);
    }


    /* Initialize the evaluation for each individual */
    for (i = 0; i < pop->N; ++i) {
        pop->members[i]->fitness = 0.0;
    }
    /*Evaluate the whole population */
    evaluator(params, current_generation, pop->members, pop->N, args);
}

/* standard implementation of tournament selection, as used by Koza
 * and most other methods of GP */
static int tournament_selection(struct gges_population *pop, int K,
                                double (*rnd)(void))
{
    int a, b;
    int i;

    a = (int)(rnd() * pop->N);
    for (i = 1; i < K; ++i) {
        b = (int)(rnd() * pop->N);
        if (pop->members[b]->fitness > pop->members[a]->fitness) {
            a = b;
        }
    }

    return a;
}

/* scans the supplied population to identify the individual with the
 * lowest fitness, starting from a random point in the population in
 * an attempt to avoid the same individual getting picked each time,
 * in the case of ties in fitness */
static int find_weakest(struct gges_population *pop, double (*rnd)(void))
{
    int i, j, start, pick;

    start = (int)(rnd() * pop->N);
    pick = start;
    for (i = 0; i < pop->N; ++i) {
        j = (i + start) % pop->N;
        if (pop->members[j]->fitness < pop->members[pick]->fitness) {
            pick = j;
        }
    }

    return pick;
}

static void generational_model(struct gges_parameters *params,
                               struct gges_bnf_grammar *grammar,
                               GGES_EVAL evaluator,
                               struct gges_population *pop,
                               struct gges_population *gen,
                               int current_generation,
                               void *args)
{
    struct gges_individual *daughter, *son;
    int i, mother, father;

    /* breed the required number of offspring. If we are preserving an
     * odd number of individuals from the previous generation, then we
     * actually have to create an additional individual as a
     * placeholder, as each crossover and/or mutation operation works
     * on two individuals to create two offspring, and so we need to
     * align with that. This placeholder offspring will get
     * overwritten in the elitism process (without being
     * evaluated!) */
    for (i = params->elitism_count - (params->elitism_count % 2); i < pop->N; i += 2) {
        /* selection of parents */
        daughter = gen->members[i];
        son      = gen->members[i + 1];

        mother = tournament_selection(pop, params->tournament_size,
                                      params->rnd);
        father = tournament_selection(pop, params->tournament_size,
                                      params->rnd);

        gges_breed(params, grammar, pop->members[mother], pop->members[father],
                   daughter, son);
    }

    /* elitism, if required */
    for (i = 0; i < params->elitism_count; ++i) {
        gges_reproduction(params, pop->members[i], gen->members[i]);
        //if (!params->cache_fitness) evaluator(params, gen->members[i], args);
    }

    /* map each individual */
    for (i = params->elitism_count; i < pop->N; ++i) {
        /* map the individuals, if not straight copies of their
         * parents */
        if (!gen->members[i]->mapped) gges_map_individual(params, grammar, gen->members[i]);
    }

    /* Initialize the evaluation for each individual */
    for (i = 0; i < pop->N; ++i) {
        gen->members[i]->fitness = 0.0;
    }

    /*Evaluate the whole population */
    evaluator(params, current_generation, gen->members, pop->N, args);
}

static void steady_state_model(struct gges_parameters *params,
                               struct gges_bnf_grammar *grammar,
                               GGES_EVAL evaluator,
                               struct gges_population *pop,
                               int current_generation,
                               void *args)
{
    struct gges_individual *daughter, *son, *offspring;
    int i, mother, father, replace;

    daughter = gges_create_individual(params);
    son = gges_create_individual(params);

    for (i = 0; i < pop->N; i += 2) {
        /* selection of parents */
        mother = tournament_selection(pop, params->tournament_size,
                                      params->rnd);
        father = tournament_selection(pop, params->tournament_size,
                                      params->rnd);

        gges_breed(params, grammar, pop->members[mother], pop->members[father],
                   daughter, son);

        /* map the individuals, if not straight copies of their
         * parents */
        if (!daughter->mapped) gges_map_individual(params, grammar, daughter);
        if (!son->mapped) gges_map_individual(params, grammar, son);


        /* evaluation
         *
         * evaluation only takes place if the individual
         * successfully mapped, and they have not been evaluated
         * already (i.e., they are not straight copies of their
         * parents) */
        if (daughter->mapped && !daughter->evaluated) {
            //daughter->fitness = evaluator(params, daughter, args);
            daughter->evaluated = true;
        } else {
            daughter->fitness = GGES_WORST_FITNESS;
            daughter->evaluated = false;
        }

        if (son->mapped && !son->evaluated) {
            //son->fitness = evaluator(params, son, args);
            son->evaluated = true;
        } else {
            son->fitness = GGES_WORST_FITNESS;
            son->evaluated = false;
        }

        /* replacement - as per GEVA, the weakest of the current
         * population is replaced with the stronger of the two
         * offspring, so long as that offspring is fitter than the
         * current weakest */
        offspring = (daughter->fitness > son->fitness) ? daughter : son;
        replace = find_weakest(pop, params->rnd);

        if (offspring->fitness > pop->members[replace]->fitness) {
            gges_reproduction(params, offspring, pop->members[replace]);
        }
    }

    gges_release_individual(daughter);
    gges_release_individual(son);
}


static bool random_search_model(struct gges_parameters *params,
                                struct gges_bnf_grammar *grammar,
                                GGES_EVAL evaluator,
                                struct gges_population *pop,
                                struct gges_population *gen,
                                int current_generation,
                                void *args)
{
    int i, w;
    static long counter = 0;
    static bool grow = false;
    int def_depth, min_depth, max_depth, depth_range;

    min_depth = params->init_min_depth;
    def_depth = params->init_max_depth;
    max_depth = params->maximum_tree_depth;
    depth_range = 1 + max_depth - min_depth;

    w = 0;
    for (i = 0; i < params->population_size; ++i) {
        if (params->sensible_initialisation) {
            params->init_max_depth = min_depth + (i % depth_range);
            if ((counter % depth_range) == 0) grow = !grow;
            if (grow) {
                params->init_min_depth = min_depth;
            } else {
                params->init_min_depth = params->init_max_depth;
            }
        } else {
            params->init_max_depth = max_depth;
        }

        gges_init_individual(params, grammar, gen->members[i]);

    }

    /* Initialize the evaluation for each individual */
    for (i = 0; i < pop->N; ++i) {
        gen->members[i]->fitness = 0.0;
    }
    /*Evaluate the whole population */
    evaluator(params, current_generation, gen->members, pop->N, args);

    for (i = 0; i < pop->N; ++i) {
        if (gen->members[i]->fitness < gen->members[w]->fitness) {
            w = i;
        }
    }

    if (pop->members[0]->fitness > gen->members[w]->fitness) {
        gges_reproduction(params, pop->members[0], gen->members[w]);
    }
    params->init_min_depth = min_depth;
    params->init_max_depth = def_depth;

    return true;
}


struct gges_population *gges_run_system(struct gges_parameters *params,
                                        struct gges_bnf_grammar *grammar,
                                        GGES_EVAL evaluator,
                                        GGES_BEFORE_GENERATION before_gen,
                                        GGES_AFTER_GENERATION after_gen,
                                        void *args)
{
    struct gges_population *pop, *gen, *tmp;
    int g = 0;

    /* create initial population */
    pop = create_population(params);
    gen = create_population(params);

    if (before_gen) before_gen(params, g, pop->members, pop->N, args);

    if (params->sensible_initialisation) {
        initialise_population_rhh(params, grammar, pop, evaluator, g, args);
    } else {
        initialise_population_rnd(params, grammar, pop, evaluator, g, args);
    }

    /* sort the population */
    qsort(pop->members, pop->N, sizeof(struct ggen_individual *),
          compare_individuals);

    if (after_gen) after_gen(params, g, false, pop->members, pop->N, args);

    for (g = 1; g <= params->generation_count; ++g) {


        if (before_gen) before_gen(params, g, pop->members, pop->N, args);

        if (params->generation_method == RANDOM_SEARCH) {
            random_search_model(params, grammar, evaluator, pop, gen, g, args);
            tmp = pop;
            pop = gen;
            gen = tmp;
        } else if (params->generation_method == GENERATIONAL) {
            generational_model(params, grammar, evaluator, pop, gen, g, args);
            tmp = pop;
            pop = gen;
            gen = tmp;
        } else if (params->generation_method == STEADY_STATE) {
            steady_state_model(params, grammar, evaluator, pop, g, args);
        } else {
            if (params->iteration == NULL) {
                fprintf(stderr,
                        "%s:%d - ERROR! Custom iteration method not supplied\n", __FILE__, __LINE__);
                exit(EXIT_FAILURE);
            } else {
                if (params->iteration(params, grammar, evaluator, pop, gen, args)) {
                    tmp = pop;
                    pop = gen;
                    gen = tmp;
                }
            }
        }

        /* sort the population */
        qsort(pop->members, pop->N, sizeof(struct ggen_individual *),
              compare_individuals);


        if (after_gen) after_gen(params, g, false, pop->members, pop->N, args);


    }

    gges_release_population(gen);

    return pop;
}


void gges_release_population(struct gges_population *pop)
{
    if (pop == NULL) return;

    while (pop->N--) gges_release_individual(pop->members[pop->N]);
    free(pop->members);
    free(pop);
}

static double rnd()
{
    return (double)rand() / (double)(1.0 + RAND_MAX);
}

/*******************************************************************************
 * Public function implementations
 ******************************************************************************/
struct gges_parameters *gges_default_parameters()
{

    struct gges_parameters *def;

    def = ALLOC(1, sizeof(struct gges_parameters), false);

    def->population_size = 100;
    def->generation_count = 50;

    def->model = CONTEXT_FREE_GP;
    def->generation_method = GENERATIONAL;
    def->elitism_count = 1;

    def->cache_fitness = true;

    def->tournament_size = 3;

    def->crossover_rate = 0.9;
    def->mutation_rate = 0.1;

    def->sensible_initialisation = true;

    /* use the grammar to work out the smallest tree depth, otherwise,
     * use Koza's recommendations for tree initialisation depths */
    def->init_min_depth = 0;
    def->init_max_depth = 6;

    def->init_codon_count_min = -1; /* use fixed initial codon count */
    def->init_codon_count = 200;

    def->sensible_init_tail_length = 0.5; /* this comes from GEVA */

    def->mapping_wrap_count = 0;

    def->fixed_point_crossover = false;
    def->node_selection_method = PICK_NODE_KOZA_90_10;
    def->maximum_tree_depth = 17;
    def->maximum_mutation_depth = 4;

    /**
     *--------------------------------------------------------------------------*
     *--------------------------------------------------------------------------*
     * MODIFICATION FOR IMPLEMENTATION OF CFG-GP TO EVOLVE MACHINE LEARNING
     * ALGORITHM FROM SKLEARN
     */
    //Default directory for training and test sets:
    def->dataTraining = " ";
    def->dataTest = " ";
    //Default seed to use to control the randomic behaviour of the GP:
      def->seed = 2;
    //Default directory for the grammar:
    def->grammarDir = " ";
    //Default seed to control resample over the generations:
    def->dataSeed = 0;
    //Default number of folds in the internal cross-validation (training and validation sets):
    def->internalCV = 3;
    //Default number of cores to be used on the algorithm execution
    def->nCores = 1;
    //Default time to execute each individual of the GP on evaluation
    def->timeout= 300;
    //Default exported pipeline name
    def->export_name = "pipeline.py";
    //Default verbosity level
    def->verbosity = 1;
    //Defaul track individuals variable
    def->track_ind = 1;
    //Default metric to be used by the GGP
    def->metric = "f1_weighted";

    /**
     *--------------------------------------------------------------------------*
     *--------------------------------------------------------------------------*
     */

     /* initialize random seed: */
     srand (def->seed);

    def->rnd = rnd;

    return def;
}
