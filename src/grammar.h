#ifndef GGES_GRAMMAR
#define GGES_GRAMMAR

#ifdef __cplusplus
extern "C" {
#endif

    #include <stdio.h>
    #include <stdbool.h>

    /***************************************************************************
     * Structure definitions
     **************************************************************************/
    typedef char *(*gges_bnf_data_field_generator)(double (*rnd)(void));

    /* structure to hold information about a single token in a given
     * production - a token can be either a terminal (i.e., is emitted
     * into the final string), or a non-terminal that requires further
     * expansion */
    struct gges_bnf_token {
        /* a simple flag to determine if this token is a terminal
         * (i.e., should be printed directly in the destination
         * stream), or is a non-terminal (i.e., should be expanded
         * using the appropriate non-terminal production) */
        bool terminal;

        /* a simple flag to determine is this token should be
         * expressed by emitting the data associated with the node
         * within the derivation tree (e.g., for ephemeral random
         * constants) */
        bool data_field;

        /* the actual symbol that will get printed in the stream, if
         * the token is a terminal */
        char *symbol;

        /* a pointer to the non-terminal referenced by this token. If
         * the token is in fact a terminal, then this element is
         * NULL */
        struct gges_bnf_non_terminal *nt;
    };

    /* structure to encapsulate the information required for a
     * production - it is essentially a container for a sequence of
     * tokens that */
    struct gges_bnf_production {
        int id;                        /* the unique id of the
                                        * production, with respect to
                                        * the owning non-terminal */

        struct gges_bnf_non_terminal *nt;

        int size;                      /* the number of tokens in the
                                        * current production */

        struct gges_bnf_token *tokens; /* the array of tokens */

        int min_depth;                 /* the minimum depth (i.e., the
                                        * amount of non-terminal
                                        * expansion) required to
                                        * complete this production,
                                        * including the recursive
                                        * expansion of any nested
                                        * non-terminals */

        bool recursive;
    };

    /* structure to hold information about a given non-terminal in the
     * current BNF grammar. It is essentially a container for a
     * sequence of productions that can be used to expand this
     * non-terminal */
    struct gges_bnf_non_terminal {
        int id;                        /* the unique id of the
                                        * non-terminal, with respect
                                        * to the owning grammar */

        char *label;                   /* the label of the
                                        * non-terminal, as it appears
                                        * in the grammar */

        int size;                      /* the number of productions
                                        * that can be used to expand
                                        * this non-terminal,
                                        * equivalent to the length of
                                        * the array below */

        struct gges_bnf_production *productions;

        int min_depth;                 /* the minimum depth of all the
                                        * productions associated with
                                        * this non-terminal */

        bool recursive;                /* true if any of the
                                        * productions labelled with
                                        * this non-terminal are
                                        * recursive (i.e., through
                                        * their expansion they refer
                                        * back to this non-terminal */
    };

    struct gges_bnf_grammar {
        char **data_field_gen_keys;
        gges_bnf_data_field_generator *data_field_gen_fn;
        int data_field_gen_n;

        int size; /* the number of non-terminals in the grammar */

        /* a collection of the non-terminals in the grammar */
        struct gges_bnf_non_terminal *non_terminals;

        /* the start symbol for the grammar, or set to NULL to use the
         * first element of the non-terminal array */
        struct gges_bnf_non_terminal *start;
    };


    struct gges_bnf_grammar *gges_create_empty_grammar();

    void gges_register_data_field_generator(struct gges_bnf_grammar *g, char *key, gges_bnf_data_field_generator fn);

    /* reads a file containing a BNF grammar specification, and returns the
     * corresponding data structure
     */
    struct gges_bnf_grammar *gges_load_bnf(const char *file_name);
    void gges_write_bnf(FILE *f, struct gges_bnf_grammar *g);

    /* constructs a suitable grammar object from the given BNF string
     */
    struct gges_bnf_grammar *gges_parse_bnf(const char *bnfstr);

    void gges_extend_grammar(struct gges_bnf_grammar *g,
                             const char *bnfstr, bool relink);

    /* BNF grammar destructor */
    void gges_release_grammar(struct gges_bnf_grammar *g);

    void gges_print(FILE *f, struct gges_bnf_grammar *g);

    bool gges_grammar_has_non_terminal(struct gges_bnf_grammar *g, char *key);

    int gges_query_productions(struct gges_bnf_production **res,
                               struct gges_bnf_non_terminal *nt,
                               int max_depth, bool recursive_only);

    int gges_query_productions(struct gges_bnf_production **res,
                               struct gges_bnf_non_terminal *nt,
                               int max_depth, bool recursive_only);

    char *gges_bnf_init_data_field(struct gges_bnf_grammar *g, char *key, double (*rnd)(void));

#ifdef __cplusplus
}
#endif

#endif
