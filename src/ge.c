#include <stdlib.h>

#include <string.h>

#include "grammar.h"
#include "ge.h"

#include "alloc.h"

#define CODON_INC 1024



/*******************************************************************************
 * internal helper function prototypes
 ******************************************************************************/
static int map_sequence(struct gges_mapping *m,
                        struct gges_ge_codon_list *l,
                        struct gges_bnf_non_terminal *nt,
                        int *wraps, int offset);

static int map_derivation(struct gges_derivation_tree **dest,
                          struct gges_bnf_grammar *g,
                          struct gges_ge_codon_list *list,
                          struct gges_bnf_non_terminal *nt,
                          int wraps, int offset);

static bool sensible_init(struct gges_ge_codon_list *list,
                          struct gges_bnf_non_terminal *nt,
                          int depth, int min_depth, int max_depth,
                          double (*rnd)(void));





/*******************************************************************************
 * Public function implementations
 ******************************************************************************/
struct gges_ge_codon_list *gges_ge_create_codon_list()
{
    struct gges_ge_codon_list *list;

    list = ALLOC(1, sizeof(struct gges_ge_codon_list), false);
    list->codons = NULL;
    list->N = 0;
    list->sz = 0;

    return list;
}

void gges_ge_release_codon_list(struct gges_ge_codon_list *list)
{
    free(list->codons);
    free(list);
}



bool gges_ge_random_init(struct gges_bnf_grammar *g,
                         struct gges_ge_codon_list *list,
                         int codon_count,
                         double (*rnd)(void))
{
    int i;

    free(list->codons);
    list->sz = sizeof(gges_ge_codon) * CODON_INC;

    list->codons = ALLOC(CODON_INC, sizeof(gges_ge_codon), false);
    for (i = 0; i < codon_count; ++i) {
        list->codons[i] = (gges_ge_codon)(rnd() * MAX_CODON_VALUE);
    }
    list->N = codon_count;

    return true;
}



bool gges_ge_sensible_init(struct gges_bnf_grammar *g,
                           struct gges_ge_codon_list *list,
                           int min_depth, int max_depth,
                           double tail_length,
                           double (*rnd)(void))
{
    struct gges_bnf_non_terminal *start;
    int tail_codons;

    if (g->start == NULL) {
        /* the supplied grammar has no explicitly nominated start
         * symbol, so we will use the first defined non-terminal as
         * our starting point */
        start = g->non_terminals + 0;
    } else {
        start = g->start;
    }

    free(list->codons);
    list->sz = sizeof(gges_ge_codon) * CODON_INC;

    list->codons = ALLOC(CODON_INC, sizeof(gges_ge_codon), false);

    list->N = 0;
    if (sensible_init(list, start, 1, min_depth, max_depth, rnd)) {
        /* add a random tail to the genome, if required */
        tail_codons = (int)((1 + tail_length) * list->N);
        while (list->N < tail_codons) {
            if (list->sz <= (list->N * sizeof(gges_ge_codon))) {
                list->sz += CODON_INC * sizeof(gges_ge_codon);
                list->codons = REALLOC(list->codons, 1, list->sz);
            }
            list->codons[list->N++] = (gges_ge_codon)(rnd() * MAX_CODON_VALUE);
        }

        return true;
    } else {
        return false;
    }
}




bool gges_ge_map_codons(struct gges_bnf_grammar *g,
                        struct gges_ge_codon_list *list,
                        struct gges_mapping *mapping,
                        int wraps)
{
    struct gges_bnf_non_terminal *start;

    if (g->start == NULL) {
        /* the supplied grammar has no explicitly nominated start
         * symbol, so we will use the first defined non-terminal as
         * our starting point */
        start = g->non_terminals + 0;
    } else {
        start = g->start;
    }

    /* the mapping function will return less than zero if there was a
     * problem decoding the individual, most likely because the codon
     * sequence did not lead to a valid individual */
    return map_sequence(mapping, list, start, &wraps, 0) >= 0;
}



struct gges_derivation_tree *gges_ge_derive(struct gges_bnf_grammar *g,
                                            struct gges_ge_codon_list *list,
                                            int wraps)
{
    struct gges_derivation_tree *dt;
    struct gges_bnf_non_terminal *start;

    if (g->start == NULL) {
        /* the supplied grammar has no explicitly nominated start
         * symbol, so we will use the first defined non-terminal as
         * our starting point */
        start = g->non_terminals + 0;
    } else {
        start = g->start;
    }

    map_derivation(&dt, g, list, start, wraps, 0);

    return dt;
}



void gges_ge_reproduction(struct gges_ge_codon_list *p,
                          struct gges_ge_codon_list *o)
{
    size_t reqsz;

    reqsz = (p->N * sizeof(gges_ge_codon));
    /* check that the destination buffer for the genome is sufficient,
     * and resize if necessary */
    if (o->sz < reqsz) {
        while (o->sz < reqsz) o->sz += CODON_INC * sizeof(gges_ge_codon);

        o->codons = REALLOC(o->codons, 1, o->sz);
    }

    o->N = p->N;
    memcpy(o->codons, p->codons, reqsz);
}

void gges_ge_crossover(struct gges_ge_codon_list *m,
                       struct gges_ge_codon_list *f,
                       struct gges_ge_codon_list *d,
                       struct gges_ge_codon_list *s,
                       bool fixed_point,
                       double (*rnd)(void))
{
    int cpm, cpf;
    size_t newsz;

    /* pick crossover sites in the parents */
    if (fixed_point) {
        if (m->N < f->N) {
            cpm = (int)(rnd() * m->N);
        } else {
            cpm = (int)(rnd() * f->N);
        }
        cpf = cpm;
    } else {
        cpm = (int)(rnd() * m->N);
        cpf = (int)(rnd() * f->N);
    }

    /* work out the offspring size */
    d->N = cpm + f->N - cpf;
    s->N = cpf + m->N - cpm;

    /* check that the offspring genome buffers are big enough, and
     * resize if needed */
    newsz = d->N * sizeof(gges_ge_codon);
    if (newsz > d->sz) {
        while (d->sz < newsz) d->sz += CODON_INC * sizeof(gges_ge_codon);
        d->codons = REALLOC(d->codons, 1, d->sz);
    }

    newsz = s->N * sizeof(gges_ge_codon);
    if (newsz > s->sz) {
        while (s->sz < newsz) s->sz += CODON_INC * sizeof(gges_ge_codon);
        s->codons = REALLOC(s->codons, 1, s->sz);
    }

    /* perform the crossover */
    memcpy(d->codons, m->codons, cpm * sizeof(gges_ge_codon));
    memcpy(d->codons + cpm, f->codons + cpf,
           (f->N - cpf) * sizeof(gges_ge_codon));

    memcpy(s->codons, f->codons, cpf * sizeof(gges_ge_codon));
    memcpy(s->codons + cpf, m->codons + cpm,
           (m->N - cpm) * sizeof(gges_ge_codon));
}

void gges_ge_mutation(struct gges_ge_codon_list *list,
                      double pm, double (*rnd)(void))
{
    int i;

    for (i = 0; i < list->N; ++i) {
        if (rnd() < pm) {
            list->codons[i] = (gges_ge_codon)(rnd() * MAX_CODON_VALUE);
        }
    }
}

bool gges_ge_breed(struct gges_ge_codon_list *m,
                   struct gges_ge_codon_list *f,
                   struct gges_ge_codon_list *d,
                   struct gges_ge_codon_list *s,
                   bool fixed_point,
                   double pc, double pm,
                   double (*rnd)(void))
{
    if (rnd() < pc) {
        gges_ge_crossover(m, f, d, s, fixed_point, rnd);
    } else {
        gges_ge_reproduction(m, d);
        gges_ge_reproduction(f, s);
    }

    gges_ge_mutation(d, pm, rnd);
    gges_ge_mutation(s, pm, rnd);

    return false;
}










/*******************************************************************************
 * internal helper function implementations
 ******************************************************************************/
static int map_sequence(struct gges_mapping *m,
                        struct gges_ge_codon_list *l,
                        struct gges_bnf_non_terminal *nt,
                        int *wraps, int offset)
{
    int i;
    struct gges_bnf_production *p;

    if (offset < 0) return -1;

    /* fix the wrapping, if we have run out of codons in the current genome */
    if (offset == l->N) {
        if (*wraps == 0) return -1; /* failed to decode properly */

        offset = 0;
        (*wraps)--;
    }

    if (nt->size == 1) {
        /* no choice to make, just move to the next non-terminal */
        p = nt->productions + 0;
    } else {
        /* use the MOD operator to work out the next required
         * production */
        p = nt->productions + (l->codons[offset] % nt->size);

        /* we have consumed a codon, so increment the pointer */
        offset++;
    }

    for (i = 0; i < p->size; ++i) {
        if (p->tokens[i].terminal) {
            /* current token is a terminal, and needs to be printed
             * into the destination stream */
            gges_mapping_append_symbol(m, p->tokens[i].symbol);
        } else {
            /* the current token is a non-terminal, and so needs
             * further expansion. We do this via a recursive call to
             * the relevant production of the corresponding
             * non-terminal */
            offset = map_sequence(m, l, p->tokens[i].nt, wraps, offset);
        }
    }

    return offset;
}



static int map_derivation(struct gges_derivation_tree **dest,
                          struct gges_bnf_grammar *g,
                          struct gges_ge_codon_list *list,
                          struct gges_bnf_non_terminal *nt,
                          int wraps, int offset)
{
    int i;
    struct gges_bnf_production *p;
    struct gges_derivation_tree *dt, *sub;

    *dest = NULL;
    /* the offset will be zero if there was a problem with
     * decoding the genome, at which point we need to stop the
     * decoding process abruptly */
    if (offset < 0) return -1;

    /* fix the wrapping, if we have run out of codons in the current genome */
    if (offset == list->N) {
        if (wraps == 0) return -1; /* failed to decode properly */

        offset = 0;
        wraps--;
    }

    if (nt->size == 1) {
        /* no choice to make, just move to the next non-terminal */
        p = nt->productions + 0;
    } else {
        /* use the MOD operator to work out the next required
         * production */
        p = nt->productions + (list->codons[offset] % nt->size);

        /* we have consumed a codon, so increment the pointer */
        offset++;
    }

    /* create a new element in the derivation tree, rooted with the
     * current non-terminal */
    *dest = dt = gges_create_derivation_tree(p->size);
    dt->label = ALLOC(strlen(nt->label) + 1, sizeof(char), false);
    strcpy(dt->label, nt->label);

    /* then, copy each token in the current production into the
     * derivation tree */
    for (i = 0; i < p->size; ++i) {
        /* if the current token is a terminal, then place a single
         * element into the derivation tree containing the current
         * symbol, otherwise, we need to recursively build the
         * required derivation tree for the non-terminal symbol */
        if (p->tokens[i].terminal) {
            sub = gges_create_derivation_tree(0);
            sub->label = ALLOC(strlen(p->tokens[i].symbol) + 1, sizeof(char), false);
            strcpy(sub->label, p->tokens[i].symbol);
        } else {
            offset = map_derivation(&sub, g, list, p->tokens[i].nt,
                                    wraps, offset);
            if (sub == NULL) { /* derivation has failed */
                sub = gges_create_derivation_tree(0);
                sub->label = ALLOC(strlen(p->tokens[i].symbol) + 2, sizeof(char), false);
                strcpy(sub->label, p->tokens[i].symbol);
                strcat(sub->label, "!");
            }
        }
        gges_add_sub_derivation(dt, sub);
    }

    return offset;
}



static bool sensible_init(struct gges_ge_codon_list *list,
                          struct gges_bnf_non_terminal *nt,
                          int depth, int min_depth, int max_depth,
                          double (*rnd)(void))
{
    int i, np, reqd;
    struct gges_bnf_production **choices, *p;
    bool success, recursive;

    /* allocate the required structures to hold the query results */
    choices = ALLOC(nt->size, sizeof(struct gges_bnf_production *), false);

    /* there are two pathways to picking "recursive" productions: the
     * first is that we are still in "full" mode (i.e., we have not
     * yet fulfilled our minimum depth requirements; otherwise,
     * recursive productions are picked with 50% probability, as per
     * Ryan and Azad (2003) */
    recursive = (depth < min_depth) | (rnd() < 0.5);

    /* our required depth is simply the difference between how far
     * down the tree we are, and how deep the tree can be */
    reqd = (max_depth - depth) + 1;

    /* lookup suitable productions based upon our current
     * non-terminal, the required minimum depth threshold, and whether
     * or not we chose recursive or non-recursive productions */
    np = gges_query_productions(choices, nt, reqd, recursive);

    /* if we could not find any suitable productions, then try
     * again, including non-recursive productions */
    if (np == 0) np = gges_query_productions(choices, nt, reqd, false);

    /* if we could not find any suitable productions, then try again,
     * but this time only productions that complete as terminals */
    if (np == 0) np = gges_query_productions(choices, nt, 1, false);

    if (np == 0) {
        /* if no required productions exist, then return false to
         * denote failure. This might happen if we asked for a tree of
         * (for example) depth 4 when the minimum depth that we can
         * produce from the grammar is (say) 7
         *
         * needless to say, this should never happen in practice, as
         * the user should be aware of the depth requirements of the
         * grammar */
        fprintf(stderr, "%s:%d - WARNING: Failed to create a tree due to "
                "insufficient remaining depth. Halted at depth %d.\n",
                __FILE__, __LINE__, depth);
        success = false;
    } else {
        /* select one of the production choices at random, then
         * "unmod" it and insert into the genome so that it can be
         * looked up later when the genotype needs to be mapped */
        p = choices[(int)(rnd() * np)];

        if (nt->size > 1) {
            /* in this case, there is more than one available
             * production, so we need to enter the choice into the
             * genome in an "unmodded" form */

            /* first, make sure that there is available space for the
             * codon, and if not, then expand the individuals genome
             * to handle it */
            if (list->sz < ((list->N + 1) * sizeof(gges_ge_codon))) {
                list->sz += CODON_INC * sizeof(gges_ge_codon);
                list->codons = REALLOC(list->codons, 1, list->sz);
            }

            i = MAX_CODON_VALUE / nt->size;
            list->codons[list->N++] = p->id + (nt->size * (int)(rnd() * i));
        }

        /* now that we have a valid production, scan through all its
         * tokens, and for any non-terminals, recursively call the
         * sensible init function from this point */
        success = true;
        for (i = 0; i < p->size; ++i) {
            if (p->tokens[i].terminal) continue;
            success = sensible_init(list, p->tokens[i].nt,
                                    depth + 1, min_depth, max_depth,
                                    rnd);
            if (!success) break;
        }
    }

    /* cleanup */
    free(choices);

    return success;
}
