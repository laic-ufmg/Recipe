#ifndef GGES_GE
#define GGES_GE

#ifdef __cplusplus
extern "C" {
#endif

    #include <stdbool.h>
    #include <limits.h>

    #include "grammar.h"
    #include "derivation.h"
    #include "mapping.h"

    /* defines the data type used for codons in the GE system. */
    #define MAX_CODON_VALUE INT_MAX
    /* #define MAX_CODON_VALUE 255 */
    typedef int gges_ge_codon;

    struct gges_ge_codon_list {
        /* the representation used in GE is essentially a
         * variable-length list of integers (a bitstring is also used
         * in the earlier work for GE, but this appears to be optional
         * in later work */
        gges_ge_codon *codons;
        int N; /* the number of codons used */
        size_t sz; /* the size of the buffer to hold the codons */
    };

    struct gges_ge_codon_list *gges_ge_create_codon_list();
    void gges_ge_release_codon_list(struct gges_ge_codon_list *list);


    /* runs the process that maps the codon list into the
     * corresponding executable code via the supplied grammar
     *
     * returns true if the mapping process was successful, otherwise
     * false */
    bool gges_ge_map_codons(struct gges_bnf_grammar *g,
                            struct gges_ge_codon_list *list,
                            struct gges_mapping *mapping,
                            int wraps);

    /* uses a simple initialisation method that generates a required
     * number of random codon values. The last parameter is a
     * pseudorandom number generator function pointer that returns
     * values in [0,1) */
    bool gges_ge_random_init(struct gges_bnf_grammar *g,
                             struct gges_ge_codon_list *list,
                             int codon_count,
                             double (*rnd)(void));

    /* uses a "sensible" initialisation method that works back from
     * the derivation tree to create the required genome. The last
     * parameter is a pseudorandom number generator function pointer
     * that returns values in [0,1) */
    bool gges_ge_sensible_init(struct gges_bnf_grammar *g,
                               struct gges_ge_codon_list *list,
                               int min_depth, int max_depth,
                               double tail_length,
                               double (*rnd)(void));
    struct gges_derivation_tree *gges_ge_derive(struct gges_bnf_grammar *g,
                                                struct gges_ge_codon_list *list,
                                                int wraps);

    void gges_ge_reproduction(struct gges_ge_codon_list *p,
                              struct gges_ge_codon_list *o);

    bool gges_ge_breed(struct gges_ge_codon_list *m,
                       struct gges_ge_codon_list *f,
                       struct gges_ge_codon_list *d,
                       struct gges_ge_codon_list *s,
                       bool fixed_point,
                       double pc, double pm,
                       double (*rnd)(void));

#ifdef __cplusplus
}
#endif

#endif
