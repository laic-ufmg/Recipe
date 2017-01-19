#ifndef GGES_CFGGP
#define GGES_CFGGP

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <limits.h>

#include "grammar.h"
#include "derivation.h"
#include "mapping.h"
#include "gges.h"


    /* representation of the CFG-GP system. Each individual has a
     * structure that represents a derivation tree in which the
     * terminal nodes have been removed. This derivation tree can then
     * be quickly executed to produce the required instance of the
     * grammar */
    struct gges_cfggp_node {
        /* the production used at this point in the derivation tree */
        struct gges_bnf_production *p;

        int depth;  /* the depth of the derivation tree at this point */

        int num_nt; /* the number of non-terminal tokens for the
                     * production of this node */

        int size;   /* the number of non-terminal nodes in the tree
                     * rooted by this node */

        /* pointers to the subtrees that will be used to expand the
         * non-terminal components of this production */
        struct gges_cfggp_node **children;

        /* the parent of the current node (NULL if the root) */
        struct gges_cfggp_node *parent;

        /* this allows custom data (e.g., the value instantiated as
         * part of an ephemeral random constant) to be embedded into
         * the node so that it can be expressed into the sentence that
         * gets produced from this tree */
        char **data_fields;
    };

    /* constructor and destructor for CFG-GP trees */
    struct gges_cfggp_node *gges_cfggp_create_tree();
    

    
    void gges_cfggp_release_tree(struct gges_cfggp_node *tree);

    /* runs the process that maps the given tree into the
     * corresponding executable code via the grammar used to
     * initialise the tree */
    bool gges_cfggp_map_tree(struct gges_cfggp_node *tree, struct gges_mapping *mapping);

    /* initialises the derivation tree using Whigham's method
     * (1995). The last parameter is a pseudorandom number generator
     * function pointer that returns values in [0,1) */
    bool gges_cfggp_random_init(struct gges_bnf_grammar *g,
                                struct gges_cfggp_node **tree,
                                int max_depth,
                                double (*rnd)(void));

    /* initialises the derivation tree using the grow (when min_depth
     * < max_depth) or full method (when min_depth == max_depth) - in
     * the case of the full method, "best possible" full
     * initialisation is used (i.e., if there is no way that a branch
     * can be initialised to the full depth, then a terminal is
     * picked). The last parameter is a pseudorandom number generator
     * function pointer that returns values in [0,1) */
    bool gges_cfggp_sensible_init(struct gges_bnf_grammar *g,
                                  struct gges_cfggp_node **tree,
                                  int min_depth, int max_depth,
                                  double (*rnd)(void));

    struct gges_derivation_tree *gges_cfggp_derive(struct gges_cfggp_node *tree);

    void gges_cfggp_reproduction(struct gges_cfggp_node *parent,
                                 struct gges_cfggp_node **offspring);


    bool gges_cfggp_breed(struct gges_bnf_grammar *g,
                          struct gges_cfggp_node *mother,
                          struct gges_cfggp_node *father,
                          struct gges_cfggp_node **daughter,
                          struct gges_cfggp_node **son,
                          int mut_depth, int max_depth,
                          enum gges_cfggp_node_selection node_sel,
                          double pc, double pm,
                          double (*rnd)(void));


#ifdef __cplusplus
}
#endif

#endif
