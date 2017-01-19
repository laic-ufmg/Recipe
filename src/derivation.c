#include <stdio.h>
#include <stdlib.h>

#include <ctype.h>
#include <string.h>

#include "derivation.h"

#include "alloc.h"

struct gges_derivation_tree *gges_create_derivation_tree(int size)
{
    struct gges_derivation_tree *dt;

    dt = ALLOC(1, sizeof(struct gges_derivation_tree), false);

    dt->label = NULL;
    dt->size = size;
    dt->children = ALLOC(size, sizeof(struct gges_derivation_tree *), false);

    while (size--) dt->children[size] = NULL;

    return dt;
}

void gges_release_derivation_tree(struct gges_derivation_tree *dt)
{
    if (dt == NULL) return;

    free(dt->label);

    while (dt->size--) {
        gges_release_derivation_tree(dt->children[dt->size]);
    }

    free(dt->children);

    free(dt);
}

void gges_add_sub_derivation(struct gges_derivation_tree *parent,
                             struct gges_derivation_tree *dt)
{
    int i;

    if (parent == NULL) {
        fprintf(stderr, "%s:%d - ERROR! NULL parent passed into function.\n",
                __FILE__, __LINE__);
        return;
    }

    i = 0;
    while ((i < parent->size) && parent->children[i]) i++;

    if (i == parent->size) {
        fprintf(stderr, "%s:%d - ERROR! Parent node's capacity exceeded.\n",
                __FILE__, __LINE__);
        return;
    }

    parent->children[i] = dt;
}


static void output_node(FILE *f,
                        int pid,
                        struct gges_derivation_tree *dt,
                        char *nodeprefix,
                        int *id)
{
    int i;
    char *c;
    (*id)++;

    if (dt == NULL) return;

    if (dt->size == 0) {
        fprintf(f, "    %s%d[fontcolor=blue,label=\"", nodeprefix, *id);
    } else {
        fprintf(f, "    %s%d[label=\"", nodeprefix, *id);
    }
    for (c = dt->label; c && *c; ++c) {
        if (isspace(*c)) {
            /* spaces don't visualise well, so print an open box
             * character */
            fputs("&#9251;", f);
        } else {
            /* just dump the current character */
            fputc(*c, f);
        }
    }
    fputs("\"];\n", f);

    if (pid > 0) {
        if (dt->size == 0) {
            fprintf(f, "    %s%d->%s%d[color=blue];\n", nodeprefix, pid, nodeprefix, *id);
        } else {
            fprintf(f, "    %s%d->%s%d;\n", nodeprefix, pid, nodeprefix, *id);
        }
    }

    pid = *id;
    for (i = 0; i < dt->size; ++i) {
        output_node(f, pid, dt->children[i], nodeprefix, id);
    }
}

void gges_visualise_derivation_tree(FILE *f,
                                    struct gges_derivation_tree *dt,
                                    char *graphname, char *nodeprefix)

{
    int i;

    if (dt == NULL) return;

    if (graphname == NULL) {
        fputs("digraph DERIVATION {\n", f);
    } else {
        fprintf(f, "digraph %s {\n", graphname);
    }

    fputs("    graph[ratio=fill,center=1];\n", f);
    fputs("    node[shape=none, fontsize=48];\n\n", f);

    i = 0;
    if (nodeprefix == NULL) {
        output_node(f, -1, dt, "N", &i);
    } else {
        output_node(f, -1, dt, nodeprefix, &i);
    }

    fputs("}\n", f);

}



static void extract_tokens(struct gges_derivation_tree *dt,
                           char **buffer, size_t l)
{
    int i;

    if (dt == NULL) return;

    if (dt->size == 0) {
        if ((strlen(dt->label) + strlen(*buffer) + 1) > l) {
            l += BUFSIZ;
            *buffer = REALLOC(*buffer, l, sizeof(char));
        }

        strcat(*buffer, dt->label);
    } else {
        for (i = 0; i < dt->size; ++i) {
            if (dt->children[i]) extract_tokens(dt->children[i], buffer, l);
        }
    }
}

char *gges_produce_derivation(struct gges_derivation_tree *dt)
{
    char *buffer;

    buffer = ALLOC(BUFSIZ, sizeof(char), false);

    buffer[0] = '\0';
    extract_tokens(dt, &buffer, BUFSIZ);

    return buffer;
}



int gges_derivation_tree_size(struct gges_derivation_tree *dt)
{
    int i, s;

    if (dt == NULL) return 0;

    s = 1; /* size of terminal node is 1 */
    for (i = 0; i < dt->size; ++i) {
        s += gges_derivation_tree_size(dt->children[i]);
    }
    return s;
}



int gges_derivation_tree_depth(struct gges_derivation_tree *dt)
{
    int i, d, s;

    if (dt == NULL) return -1;

    d = 0; /* depth of terminal node is zero */
    for (i = 0; i < dt->size; ++i) {
        s = gges_derivation_tree_depth(dt->children[i]) + 1;
        if (s > d) d = s;
    }
    return d;
}



int gges_derivation_edit_distance(struct gges_derivation_tree *a,
                                  struct gges_derivation_tree *b)
{
    /* to be completed */
    return 0;
}
