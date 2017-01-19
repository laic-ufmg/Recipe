#ifndef GGES_INDIVIDUAL
#define GGES_INDIVIDUAL

#ifdef __cplusplus
extern "C" {
#endif

    #include <stdbool.h>
    #include <float.h>

    #include "gges.h"
    #include "mapping.h"
    #include "cfggp.h"
    #include "ge.h"

    #define GGES_WORST_FITNESS (-DBL_MAX)

    /* represents an individual in the GE system. Each individual has
     * a linear genotype that (in conjunction with a supplied grammar)
     * maps to a string that serves as the executable phenotype for
     * the individual */
    struct gges_individual {
        /* representation choice for the individual, either a string
         * of integers for GE, or a tree for CFG-GP */
        enum gges_model_type type;
        union {
            struct gges_ge_codon_list *list;
            struct gges_cfggp_node *tree;
        } representation;

        /* structure to hold the mapping from "genotype" to
         * "phenotype" */
        struct gges_mapping *mapping;

        /* reset to false whenever the genotype of the individual is
         * disrupted (e.g., through crossover, mutation, or
         * initialisation): flags that the mapping needs updating */
        bool mapped;

        /* reset to false whenever individual needs evaluating */
        bool evaluated;

        double objective; /* the score of the individual as measured
                           * against the problem, can be defined as
                           * user chooses */

        double fitness;   /* the fitness of the individual as used by
                           * the selection methods. Here, fitness is
                           * increasing, with a lower bounds of zero
                           * to denote worst possible fitness */
    };

    /* constructor and destructor for individuals */
    struct gges_individual *gges_create_individual(struct gges_parameters *params);
    void gges_release_individual(struct gges_individual *ind);

    void gges_init_individual(struct gges_parameters *params,
                              struct gges_bnf_grammar *g,
                              struct gges_individual *ind);

    /* runs the process that maps the individual's representation into
     * the corresponding executable code via the supplied grammar
     *
     * returns true if the mapping process was successful, otherwise
     * false */
    bool gges_map_individual(struct gges_parameters *params,
                             struct gges_bnf_grammar *g,
                             struct gges_individual *ind);

    /* builds an explicit derivation tree out of the supplied
     * individual - for CFGGP, this is merely a node-by-node copy of
     * the individual's representation, for GE, it is a codon-by-codon
     * MOD mapping into productions */
    struct gges_derivation_tree *gges_derive_individual(struct gges_parameters *params,
                                                        struct gges_bnf_grammar *g,
                                                        struct gges_individual *ind);

    /* perform a deep copy of the parent individual, including mapping
     * and fitness details */
    void gges_reproduction(struct gges_parameters *params,
                           struct gges_individual *parent,
                           struct gges_individual *clone);

    /* use representation-specific operators to create offspring based
     * upon the supplied parents */
    void gges_breed(struct gges_parameters *params,
                    struct gges_bnf_grammar *g,
                    struct gges_individual *mother,
                    struct gges_individual *father,
                    struct gges_individual *daughter,
                    struct gges_individual *son);

#ifdef __cplusplus
}
#endif

#endif
