#ifndef GGES_DERIV
#define GGES_DERIV

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>

#include "grammar.h"

    struct gges_derivation_tree {
        char *label;

        int size;
        struct gges_derivation_tree **children;
    };

    struct gges_derivation_tree *gges_create_derivation_tree(int size);

    void gges_add_sub_derivation(struct gges_derivation_tree *parent,
                                 struct gges_derivation_tree *dt);

    void gges_release_derivation_tree(struct gges_derivation_tree *dt);

    void gges_visualise_derivation_tree(FILE *f,
                                        struct gges_derivation_tree *dt,
                                        char *graphname, char *nodeprefix);

    char *gges_produce_derivation(struct gges_derivation_tree *dt);

    int gges_derivation_tree_depth(struct gges_derivation_tree *dt);

    int gges_derivation_tree_size(struct gges_derivation_tree *dt);

    int gges_derivation_edit_distance(struct gges_derivation_tree *a,
                                      struct gges_derivation_tree *b);

#ifdef __cplusplus
}
#endif

#endif
