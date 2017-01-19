#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include <ctype.h>
#include <string.h>

#include "grammar.h"

#include "alloc.h"


/*******************************************************************************
 * internal helper function prototypes
 ******************************************************************************/
static long file_length(const char *file_name);

static const char *read_token(const char *s, char **token);
static void write_token(FILE *f, const char *s);

static void process_token(struct gges_bnf_grammar *g,
                          struct gges_bnf_non_terminal **current_nt,
                          struct gges_bnf_production **current_p,
                          const char *current_token, const char *next_token);

static void link_non_terminal_tokens(struct gges_bnf_grammar *g);
static void calculate_production_recursion(struct gges_bnf_grammar *g);
static void calculate_production_depths(struct gges_bnf_grammar *g);
static void calculate_non_terminal_depths(struct gges_bnf_grammar *g);

static struct gges_bnf_non_terminal *lookup_non_terminal(
        struct gges_bnf_grammar *g, const char *label);








/*******************************************************************************
 * Public function implementations
 ******************************************************************************/
struct gges_bnf_grammar *gges_create_empty_grammar()
{
    struct gges_bnf_grammar *g;

    g = ALLOC(1, sizeof(struct gges_bnf_grammar), false);
    g->size = 0;
    g->non_terminals = NULL;
    g->start = NULL;

    g->data_field_gen_n = 0;
    g->data_field_gen_keys = NULL;
    g->data_field_gen_fn = NULL;

    return g;
}



void gges_register_data_field_generator(struct gges_bnf_grammar *g, char *key, gges_bnf_data_field_generator fn)
{
    int i;

    for (i = 0; i < g->data_field_gen_n; ++i) {
        if (strcmp(g->data_field_gen_keys[i], key) == 0) {
            /* field already exists, so overwrite the current function pointer */
            g->data_field_gen_fn[i] = fn;
            return;
        }
    }

    i = g->data_field_gen_n++;
    g->data_field_gen_keys = REALLOC(g->data_field_gen_keys, g->data_field_gen_n, sizeof(char *));
    g->data_field_gen_fn = REALLOC(g->data_field_gen_fn, g->data_field_gen_n, sizeof(gges_bnf_data_field_generator));

    g->data_field_gen_keys[i] = ALLOC((strlen(key) + 1), sizeof(char), false);
    strcpy(g->data_field_gen_keys[i], key);
    g->data_field_gen_fn[i] = fn;
}

struct gges_bnf_grammar *gges_load_bnf(const char *file_name)
{
    FILE *f;
    char *data;
    long flen;
    struct gges_bnf_grammar *g;

    flen = file_length(file_name);

    f = fopen(file_name, "r");
    if (f == NULL) {
        fprintf(stderr, "%s:%d - ERROR: Failed to open file %s\n",
                __FILE__, __LINE__, file_name);
        exit(EXIT_FAILURE);
    }

    data = ALLOC(flen + 1, sizeof(char), false);
     
    fread(data, 1, flen, f);
    data[flen] = '\0';
    fclose(f);

    g = gges_parse_bnf(data);

    

    free(data);
    return g;
}



struct gges_bnf_grammar *gges_parse_bnf(const char *bnfstr)
{
    struct gges_bnf_grammar *g;

    g = gges_create_empty_grammar();

    gges_extend_grammar(g, bnfstr, true);

    return g;
}



void gges_extend_grammar(struct gges_bnf_grammar *g,
                         const char *bnfstr, bool relink)
{
    char *cur, *nxt;
    struct gges_bnf_non_terminal *nt;
    struct gges_bnf_production *p;

    nt = NULL;
    p = NULL;
    cur = NULL;
    nxt = NULL;
    bnfstr = read_token(bnfstr, &nxt);

    do {
        free(cur);
        cur = nxt;
        bnfstr = read_token(bnfstr, &nxt);

        process_token(g, &nt, &p, cur, nxt);
    } while (nxt != NULL);

    free(cur);

    if (relink) {
        link_non_terminal_tokens(g);
        calculate_production_depths(g);
        calculate_production_recursion(g);
        calculate_non_terminal_depths(g);
    }
}



void gges_release_grammar(struct gges_bnf_grammar *g)
{
    int i, j, k;
    struct gges_bnf_non_terminal *nt;
    struct gges_bnf_production *p;
    struct gges_bnf_token *t;

    if (g == NULL) return;

    for (i = 0; i < g->size; ++i) {
        nt = g->non_terminals + i;
        for (j = 0; j < nt->size; ++j) {
            p = nt->productions + j;
            for (k = 0; k < p->size; ++k) {
                t = p->tokens + k;
                free(t->symbol);
            }
            free(p->tokens);
        }
        free(nt->productions);
        free(nt->label);
    }

    free(g->non_terminals);

    for (i = 0; i < g->data_field_gen_n; ++i) free(g->data_field_gen_keys[i]);
    free(g->data_field_gen_keys);
    free(g->data_field_gen_fn);

    free(g);
}



void gges_print(FILE *f, struct gges_bnf_grammar *g)
{
    int i, j, k;
    struct gges_bnf_non_terminal *nt;
    struct gges_bnf_production *p;
    struct gges_bnf_token *t;

    for (i = 0; i < g->size; ++i) {
        nt = g->non_terminals + i;
        for (j = 0; j < nt->size; ++j) {
            p = nt->productions + j;

            fprintf(f, "(%2d.%2d): %s ::= ", nt->id, p->id, nt->label);

            for (k = 0; k < p->size; ++k) {
                t = p->tokens + k;
                if (t->terminal) {
                    fprintf(f, "%s", t->symbol);
                } else {
                    fprintf(f, "%s", t->nt->label);
                }
            }
            fprintf(f, ": (%d%s)\n", p->min_depth, p->recursive ? ":R" : "");
        }
    }
}



void gges_write_bnf(FILE *f, struct gges_bnf_grammar *g)
{
    int i, j, k;
    struct gges_bnf_non_terminal *nt;
    struct gges_bnf_production *p;
    struct gges_bnf_token *t;

    for (i = 0; i < g->size; ++i) {
        nt = g->non_terminals + i;
        fprintf(f, "%s ::=", nt->label);
        for (j = 0; j < nt->size; ++j) {
            p = nt->productions + j;

            /* if this is a choice (i.e., there is more than one
             * production for the current non-terminal), then start
             * the production on an indented new line */
            if (j > 0) fprintf(f, "\t|");

            /* print out each token in the production on a single
             * line, looking up the label of the corresponding
             * non-terminal (if required) */
            for (k = 0; k < p->size; ++k) {
                t = p->tokens + k;
                if (t->terminal) {
                    write_token(f, t->symbol);
                } else {
                    fprintf(f, " %s", t->nt->label);
                }
            }
            fprintf(f, "\n");
        }
    }
}



bool gges_grammar_has_non_terminal(struct gges_bnf_grammar *g, char *key)
{
    return lookup_non_terminal(g, key) != NULL;
}

int gges_query_productions(struct gges_bnf_production **res,
                           struct gges_bnf_non_terminal *nt,
                           int max_depth, bool recursive_only)
{
    int i, c;

    c = 0;
    for (i = 0; i < nt->size; ++i) {
        if (nt->productions[i].min_depth > max_depth) continue;
        if (recursive_only && !(nt->productions[i].recursive)) continue;

        res[c++] = nt->productions + i;
    }

    return c;
}

char *gges_bnf_init_data_field(struct gges_bnf_grammar *g, char *key, double (*rnd)(void))
{
    int i;
    for (i = 0; i < g->data_field_gen_n; ++i) {
        if (strcmp(key, g->data_field_gen_keys[i]) == 0) return g->data_field_gen_fn[i](rnd);
    }

    fprintf(stderr, "%s:%d - WARNING: Could not find data field generator with key %s, returning null\n",
            __FILE__, __LINE__, key);
    return NULL;
}









/*******************************************************************************
 * internal helper function implementations
 ******************************************************************************/
static long file_length(const char *file_name)
{
    FILE *f;
    long flen;

    f = fopen(file_name, "rb");
    fseek(f, 0L, SEEK_END);
    flen = ftell(f);
    fclose(f);

    return flen;
}



static void write_token(FILE *f, const char *s)
{
    fputs(" \'", f);
    while (s && (*s != '\0')) {
        switch (*s) {
        case '\\': fputs("\\\\", f); break;
        case '\'': fputs("\\\'", f); break;
        case '\"': fputs("\\\"", f); break;
        case '\t': fputs("\\t", f); break;
        case '\r': fputs("\\r", f); break;
        case '\n': fputs("\\n", f); break;
        case '\f': fputs("\\f", f); break;
        default: fputc(*s, f); break;
        }
        s++;
    }
    fputc('\'', f);
}

static void fix_escaping(char *token, int l)
{
    int i;
    bool shift;

    i = 0;
    while (i < l) {
        if (token[i] == '\\') {
            shift = true;

            switch (token[i + 1]) {
            case '\\': token[i] = '\\'; break;
            case '\'': token[i] = '\''; break;
            case '\"': token[i] = '\"'; break;
            case 't': token[i] = '\t'; break;
            case 'r': token[i] = '\r'; break;
            case 'n': token[i] = '\n'; break;
            case 'f': token[i] = '\f'; break;
            default:
                shift = false;
                fprintf(stderr, "%s:%d - WARNING: invalid escape "
                                "sequence found \'\\%c\'\n",
                        __FILE__, __LINE__, token[i + 1]);
                break;
            }

            if (shift) {
                memmove(token + i + 1, token + i + 2, (l - (i + 2) + 1));
                token[l--] = '\0';
            }
        }
        i++;
    }
}



static const char *move_to_next_token(const char *s)
{
    if ((s == NULL) || (*s == '\0')) return s;

    do {
        /* skip any unquoted whitespace */
        while (isspace(*s)) s++;

        /* strip comments */
        if (strncmp(s, "/*", 2) == 0) {
            s = strstr(s, "*/");
            if (s == NULL) {
                fprintf(stderr,
                        "%s:%d - Warning: Unterminated multi-line comment "
                        "in string.\n",
                        __FILE__, __LINE__);
            } else {
                s += 2;
            }

            continue;
        } else if (*s == '#' || strncmp(s, "//", 2) == 0) {
            s += strcspn(s, "\n");
            continue;
        } else {
            break;
        }
    } while (s && (*s != '\0'));

    return s;
}

static size_t find_token_end(const char *s)
{
    size_t l;
    char sep;
    if (strncmp(s, "::=", 3) == 0) {
        l = 3;
    } else if (*s == '\'' || *s == '\"') {
        sep = *s;
        l = 1;
        while (*(s+l) != sep) l += (*(s+l) == '\\') ? 2 : 1;
        if (*(s+l) != '\0') l++;
    } else if (*s == '|') {
        l = 1;
    } else if (*s == '<') {
        l = strcspn(s, ">");
        if (*(s+l) != '\0') l++;
    } else {
        l = strcspn(s, "< \t\n");
    }

    return l;
}

static char * extract_token(const char *s, size_t l)
{
    char *token;

    token = ALLOC(l + 1, sizeof(char), false);
    strncpy(token, s, l);
    token[l] = '\0';

    fix_escaping(token, l);

    return token;
}

static const char *read_token(const char *s, char **token)
{
    size_t l;

    *token = NULL;
    s = move_to_next_token(s);

    if ((s == NULL) || (*s == '\0')) return NULL;

    l = find_token_end(s);
    *token = extract_token(s, l);

    return (s + l);
}




static void append_token(struct gges_bnf_production *p, const char *token)
{
    struct gges_bnf_token *t;
    size_t l;

    p->tokens = REALLOC(p->tokens, (p->size + 1), sizeof(struct gges_bnf_token));
    t = p->tokens + p->size++;

    /* non-terminals will get hooked up later, once the grammar is
     * complete. For now, just make sure the pointer is NULL */
    t->nt = NULL;

    /* label as terminal or non-terminal */
    t->terminal = (strncmp("<", token, 1) != 0);

    /* label as a computed field, or otherwise */
    t->data_field = (strncmp("@", token, 1) == 0);

    /* get the length of the token, we'll trim it next if need be */
    l = strlen(token);

    /* a computed data field is denoted in the grammar by being
     * enclosed in @ characters (e.g., @ERC@), when the associated
     * function is registered into the system, the key is not
     * surrounded by these, so we need to strip them before adding the
     * symbol */
    if (t->data_field) {
        token++;
        l -= 2;
    }

    /* check and remove any quotes, then add the symbol */
    if (*token == '\"' || *token == '\'') {
        token++;
        l -= 2;
    }

    t->symbol = ALLOC(l + 1, sizeof(char), false);
    strncpy(t->symbol, token, l);
    t->symbol[l] = '\0';
}

static struct gges_bnf_non_terminal *lookup_non_terminal(
    struct gges_bnf_grammar *g, const char *label)
{
    int i;

    if (label == NULL) return NULL;

    for (i = 0; i < g->size; ++i) {
        if (strcmp(label, g->non_terminals[i].label) == 0) {
            return (g->non_terminals + i);
        }
    }

    return NULL;
}

static struct gges_bnf_non_terminal *create_non_terminal(
    struct gges_bnf_grammar *g, const char *label)
{
    struct gges_bnf_non_terminal *nt;

    g->non_terminals = REALLOC(g->non_terminals, (g->size + 1), sizeof(struct gges_bnf_non_terminal));
    nt = g->non_terminals + g->size;
    nt->id = g->size++;

    nt->label = ALLOC(strlen(label) + 1, sizeof(char), false);
    strcpy(nt->label, label);

    nt->size = 0;
    nt->productions = NULL;

    nt->recursive = false;

    return nt;
}

static struct gges_bnf_production *create_production(
    struct gges_bnf_non_terminal *nt)
{
    struct gges_bnf_production *p;

    nt->productions = REALLOC(nt->productions, (nt->size + 1), sizeof(struct gges_bnf_production));
    p = nt->productions + nt->size;
    p->id = nt->size++;

    p->size = 0;
    p->tokens = NULL;

    p->min_depth = 0; /* size calculation needed */
    p->recursive = false;

    return p;
}

static void process_token(struct gges_bnf_grammar *g,
                          struct gges_bnf_non_terminal **current_nt,
                          struct gges_bnf_production **current_p,
                          const char *current_token, const char *next_token)
{
    if (next_token == NULL) {
        /* the current token will be the last to process, so append it
         * to the current production and then close it off */
        append_token(*current_p, current_token);
    } else if (strncmp("::=", next_token, 3) == 0) {
        /* the current token marks the start of a new non-terminal
         * definition, so switch to the new non-terminal label */
        *current_nt = lookup_non_terminal(g, current_token);
        if (*current_nt == NULL) {
            *current_nt = create_non_terminal(g, current_token);
        }
        *current_p = create_production(*current_nt);
    } else if (strncmp("|", next_token, 1) == 0) {
        /* the current token is to be the last component of the
         * current production, and another production for the current
         * non-terminal is expected */
        append_token(*current_p, current_token);
        *current_p = create_production(*current_nt);
    } else {
        /* so long as the current token is not markup (e.g., ::=),
         * then it should be added to the current production */
        if (strncmp("::=", current_token, 3) == 0) return;
        if (strncmp("|", current_token, 1) == 0) return;

        append_token(*current_p, current_token);
    }
}










static int get_non_terminal_depth(struct gges_bnf_grammar *g,
                                  struct gges_bnf_non_terminal *nt)
{
    int i;
    int depth;

    /* assume the default position that the non-terminal cannot be
     * labelled with a minimum depth */
    depth = 0;

    for (i = 0; i < nt->size; ++i) {
        /* if we have not analysed this production, then skip */
        if (nt->productions[i].min_depth == 0) continue;

        /* if this is the first production that we have inspected,
         * then assign its minimum depth as the current representative
         * depth */
        if (depth == 0) depth = nt->productions[i].min_depth;

        /* if the current production has a minimum depth smaller than
         * that of the current representative depth, then overwrite
         * the non-terminal's representative depth */
        if (nt->productions[i].min_depth < depth) {
            depth = nt->productions[i].min_depth;
        }
    }

    return depth;
}

static void calculate_production_depths(struct gges_bnf_grammar *g)
{
    int i, j, k;
    int labelled, unlabelled;
    int prod_depth, nt_depth;

    struct gges_bnf_non_terminal *nt;
    struct gges_bnf_production *p;
    struct gges_bnf_token *t;

    do {
        labelled = unlabelled = 0;

        for (i = 0; i < g->size; ++i) {
            nt = g->non_terminals + i;
            for (j = 0; j < nt->size; ++j) {
                p = g->non_terminals[i].productions + j;

                /* if the minimum depth of the production is already
                 * known, then there is no need to recalculate it */
                if (p->min_depth > 0) continue;

                /* by definition, the smallest possible depth of a
                 * production is 1 (when it contains no non-terminal
                 * symbols) */
                prod_depth = 1;
                for (k = 0; k < p->size; ++k) {
                    t = p->tokens + k;
                    if (t->terminal) continue;

                    /* get the representative minimum depth for the
                     * current non-terminal token. The representative
                     * depth is defined as the smallest minimum depth
                     * of all the non-terminal's productions */
                    nt_depth = get_non_terminal_depth(g, t->nt);

                    if (nt_depth == 0) {
                        /* no productions for the the required
                         * non-terminal have been labelled with their
                         * minimum depth, so we do not know the
                         * representative depth for the non-terminal,
                         * and so we cannot calculate the minimum
                         * depth of this production at this stage */
                        prod_depth = 0;
                        break;
                    } else if (nt_depth >= prod_depth) {
                        prod_depth = nt_depth + 1;
                    }
                }

                if (prod_depth > 0) {
                    labelled++;
                    p->min_depth = prod_depth;
                } else {
                    unlabelled++;
                }
            }
        }

        if (labelled == 0 && unlabelled != 0) {
            fprintf(stderr,
                    "%s:%d - ERROR: Incomplete grammar specification, "
                    "cannot determine minimum depth of some non-terminals.\n",
                    __FILE__, __LINE__);
            exit(EXIT_FAILURE);
        }
    } while (labelled != 0);
}

static void calculate_production_recursion(struct gges_bnf_grammar *g)
{
    int i, j, k;
    int labelled;

    struct gges_bnf_non_terminal *nt;
    struct gges_bnf_production *p;
    struct gges_bnf_token *t;

    /* first pass, does the production use its own LHS? */
    for (i = 0; i < g->size; ++i) {
        nt = g->non_terminals + i;
        nt->recursive = false;

        for (j = 0; j < nt->size; ++j) {
            p = nt->productions + j;
            p->recursive = false;

            for (k = 0; k < p->size; ++k) {
                t = p->tokens + k;

                if (t->terminal) continue;

                if (t->nt == nt) {
                    p->recursive = true;
                    nt->recursive = true;
                    break;
                }
            }
        }
    }

    do {
        labelled = 0;
        /* second pass, does the production use a known recursive non-terminal? */
        for (i = 0; i < g->size; ++i) {
            nt = g->non_terminals + i;
            for (j = 0; j < nt->size; ++j) {
                p = nt->productions + j;
                if (p->recursive) continue;

                for (k = 0; k < p->size; ++k) {
                    t = p->tokens + k;

                    if (t->terminal) continue;

                    if (t->nt->recursive) {
                        p->recursive = true;
                        nt->recursive = true;
                        labelled++;
                        break;
                    }
                }
            }
        }
    } while (labelled != 0);
}

static void calculate_non_terminal_depths(struct gges_bnf_grammar *g)
{
    int i, j;
    struct gges_bnf_non_terminal *nt;

    for (i = 0; i < g->size; ++i) {
        nt = g->non_terminals + i;
        if (nt->size == 0) {
            fprintf(stderr,
                    "%s:%d - Warning! Non-terminal %s "
                    "does not have any defined productions.\n",
                    __FILE__, __LINE__, nt->label);
            nt->min_depth = -1;
        } else {
            nt->min_depth = nt->productions[0].min_depth;
        }

        for (j = 1; j < nt->size; ++j) {
            if (nt->productions[j].min_depth < nt->min_depth) {
                nt->min_depth = nt->productions[j].min_depth;
            }
        }
    }
}

static void link_non_terminal_tokens(struct gges_bnf_grammar *g)
{
    int i, j, k;
    struct gges_bnf_non_terminal *nt;
    struct gges_bnf_production *p;
    struct gges_bnf_token *t;

    for (i = 0; i < g->size; ++i) {
        nt = g->non_terminals + i;
        for (j = 0; j < nt->size; ++j) {
            p = nt->productions + j;

            /* setup the lookup reference to the production's parent
             * non-terminal */
            p->nt = nt;

            /* flag the current production as needing a depth check */
            p->min_depth = 0;

            /* check each token in the current production, if it is a
             * non-terminal, then hook it up to the appropriate entry
             * in the grammar, otherwise, leave the reference as
             * NULL */
            for (k = 0; k < g->non_terminals[i].productions[j].size; ++k) {
                t = p->tokens + k;
                t->nt = NULL;

                if (t->terminal) continue;

                t->nt = lookup_non_terminal(g, t->symbol);

                /* if the non-terminal is not found, then we have an
                 * incomplete grammar at thsi stage, and an error
                 * should be raised. Perhaps this could be modified in
                 * the future to include the option to create the
                 * grammar on the fly */
                if (t->nt == NULL) {
                    fprintf(stderr,
                            "%s:%d - Error! Production %d for non-terminal %s "
                            "uses an undefined non-terminal %s\n",
                            __FILE__, __LINE__, j, nt->label, t->symbol);
                    exit(EXIT_FAILURE);
                }
            }
        }
    }
}
