#include <stdlib.h>

#include <string.h>

#include "grammar.h"
#include "cfggp.h"

#include "alloc.h"




/*******************************************************************************
 * internal helper function prototypes
 ******************************************************************************/
static struct gges_cfggp_node *create_node(struct gges_bnf_production *p);

static struct gges_cfggp_node *replicate_tree(struct gges_cfggp_node *t);

static void map_sequence(struct gges_mapping *mapping,
                         struct gges_cfggp_node *t);

static struct gges_derivation_tree *map_derivation(struct gges_cfggp_node *t);

static void calculate_depths(struct gges_cfggp_node *t);



static bool sensible_init(struct gges_bnf_grammar *g,
                          struct gges_cfggp_node **t,
                          struct gges_bnf_non_terminal *nt,
                          int depth, int min_depth, int max_depth,
                          double (*rnd)(void));

static struct gges_bnf_production *random_number(struct gges_bnf_production *p,
                                                double (*rnd)(void), char *tag);

static int pick_subtree(struct gges_cfggp_node **pick,
                        struct gges_cfggp_node *parent,
                        struct gges_bnf_non_terminal *required_type,
                        enum gges_cfggp_node_selection node_sel,
                        double (*rnd)(void));

static struct gges_cfggp_node *perform_tree_swap(struct gges_cfggp_node **tree,
                                                 struct gges_cfggp_node *pick,
                                                 int pick_idx,
                                                 struct gges_cfggp_node *rep);








/*******************************************************************************
 * Public function implementations
 ******************************************************************************/

 
void gges_cfggp_release_tree(struct gges_cfggp_node *tree)
{
    int i;

    if (tree == NULL) return;

    while (tree->num_nt--) gges_cfggp_release_tree(tree->children[tree->num_nt]);

    free(tree->children);

    for (i = 0; i < tree->p->size; ++i) free(tree->data_fields[i]);
    free(tree->data_fields);

    free(tree);
}



bool gges_cfggp_map_tree(struct gges_cfggp_node *tree, struct gges_mapping *mapping)
{
    map_sequence(mapping, tree);

    return true;
}



bool gges_cfggp_random_init(struct gges_bnf_grammar *g,
                            struct gges_cfggp_node **tree,
                            int max_depth,
                            double (*rnd)(void))
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

    gges_cfggp_release_tree(*tree);
    *tree = NULL;

    if (sensible_init(g, tree, start, 1, 1, max_depth, rnd)) {
        calculate_depths(*tree);

        return true;
    } else {
        return false;
    }
}



bool gges_cfggp_sensible_init(struct gges_bnf_grammar *g,
                              struct gges_cfggp_node **tree,
                                int min_depth, int max_depth,
                                double (*rnd)(void))
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

    gges_cfggp_release_tree(*tree);
    *tree = NULL;

    if (sensible_init(g, tree, start, 1, min_depth, max_depth, rnd)) {
        calculate_depths(*tree);

        return true;
    } else {
        return false;
    }
}



struct gges_derivation_tree *gges_cfggp_derive(struct gges_cfggp_node *tree)
{
    return map_derivation(tree);
}



void gges_cfggp_reproduction(struct gges_cfggp_node *parent,
                             struct gges_cfggp_node **offspring)
{
    /* overwrite the offspring's genome with a clone of the parent */
    gges_cfggp_release_tree(*offspring);
    *offspring = replicate_tree(parent);
}



void gges_cfggp_crossover(struct gges_cfggp_node *mother,
                          struct gges_cfggp_node *father,
                          struct gges_cfggp_node **daughter,
                          struct gges_cfggp_node **son,
                          int max_depth,
                          enum gges_cfggp_node_selection node_sel,
                          double (*rnd)(void))
{
    struct gges_cfggp_node *d_cp, *s_cp, *tmp;
    int d_pidx, s_pidx;
    int d_allowed_depth, s_allowed_depth;
    bool d_ok, s_ok;

    /* first, make clones of the parents */
    gges_cfggp_reproduction(mother, daughter);
    gges_cfggp_reproduction(father, son);

    /* then, pick crossover points in the offspring. We need to loop
     * this process, as we may select a non-terminal in the first
     * offspring that does not exist in the second. As both offspring
     * will have at least one non-terminal in common (the start
     * symbol), this loop is guaranteed to terminate at some stage,
     * and will probably never exceed a single iteration in any
     * problem of reasonable complexity */
    do {
        d_pidx = pick_subtree(&d_cp, *daughter, NULL, node_sel, rnd);
        s_pidx = pick_subtree(&s_cp, *son, d_cp->p->nt, node_sel, rnd);
    } while (s_cp == NULL);

    /* and then work out how big the spliced-in trees can be in each
     * of the offspring, to ensure that we are not exceeding crossover
     * depths as defined by the system */
    if (max_depth > 0) {
        /* depth limiting is being used, so work out available depth
         * in each offspring tree */
        d_allowed_depth = max_depth;
        tmp = d_cp;
        while ((tmp = tmp->parent) != NULL) d_allowed_depth--;

        s_allowed_depth = max_depth;
        tmp = s_cp;
        while ((tmp = tmp->parent) != NULL) s_allowed_depth--;

        /* then, test the validity of each chosen crossover point */
        d_ok = s_cp->depth <= d_allowed_depth;
        s_ok = d_cp->depth <= s_allowed_depth;
    } else {
        /* if no depth limiting is used, then the offspring can be
         * crossed without examination */
        d_ok = true;
        s_ok = true;
    }

    /* finally, perform the crossover */
    if (d_ok && s_ok) {
        /* perform a straight swap of subtrees, no additional memory copying required */
        if (d_cp == *daughter) {
            *daughter = s_cp;
        } else {
            d_cp->parent->children[d_pidx] = s_cp;
        }
        if (s_cp == *son) {
            *son = d_cp;
        } else {
            s_cp->parent->children[s_pidx] = d_cp;
        }

        tmp = d_cp->parent;
        d_cp->parent = s_cp->parent;
        s_cp->parent = tmp;

        /* recalculate depths in the offspring */
        calculate_depths(*daughter);
        calculate_depths(*son);
    } else if (d_ok) {
        /* in this case, the crossover operation will result in the
         * son offspring being too large, but a daughter that is of
         * suitable size. In this case, we need to make a copy of the
         * subtree that we selected from the son, splice that into the
         * daughter, and leave the other offspring unchanged */
        s_cp = replicate_tree(s_cp);

        tmp = perform_tree_swap(daughter, d_cp, d_pidx, s_cp);
        gges_cfggp_release_tree(tmp);

        calculate_depths(*daughter);
    } else if (s_ok) {
        /* in this case, the crossover operation will result in the
         * daughter offspring being too large, but a son that is of
         * suitable size. In this case, we need to make a copy of the
         * subtree that we selected from the daughter, splice that
         * into the son, and leave the other offspring unchanged */
        d_cp = replicate_tree(d_cp);

        tmp = perform_tree_swap(son, s_cp, s_pidx, d_cp);
        gges_cfggp_release_tree(tmp);

        calculate_depths(*son);
    }
}



void gges_cfggp_mutation(struct gges_bnf_grammar *g,
                         struct gges_cfggp_node **tree,
                         double mutation_rate,
                         int mut_depth, int max_depth,
                         enum gges_cfggp_node_selection node_sel,
                         double (*rnd)(void))
{
    struct gges_cfggp_node *mp, *mut, *tmp;

    int pidx;
    int allowed_depth;

    if (rnd() > mutation_rate) return;

    /* pick a site in the tree */
    pidx = pick_subtree(&mp, *tree, NULL, node_sel, rnd);

    /* we need to ensure that the mutation of the tree does not
     * exceed the depth limits of the system. We can do this by
     * ensuring that the maximum depth of the mutant subtree is not
     * greater than the remaining availble tree depth at the point of
     * mutation */
    if (max_depth > 0) {
        allowed_depth = max_depth;
        tmp = mp;
        while ((tmp = tmp->parent) != NULL) allowed_depth--;

        if (mut_depth > allowed_depth) mut_depth = allowed_depth;
    }

    /* grow a mutant subtree using the non-terminal LHS of the
     * production of the identified site */
    sensible_init(g, &mut, mp->p->nt, 1, 1, mut_depth, rnd);

    /* swap the subtree with the mutant */
    tmp = perform_tree_swap(tree, mp, pidx, mut);

    /* cleanup the old subtree that was removed from the tree */
    gges_cfggp_release_tree(tmp);

    /* recalculate depths in the genome */
    calculate_depths(*tree);
}



bool gges_cfggp_breed(struct gges_bnf_grammar *g,
                      struct gges_cfggp_node *mother,
                      struct gges_cfggp_node *father,
                      struct gges_cfggp_node **daughter,
                      struct gges_cfggp_node **son,
                      int mut_depth, int max_depth,
                      enum gges_cfggp_node_selection node_sel,
                      double pc, double pm,
                      double (*rnd)(void))
{
    double p;

    p = rnd();
    if (p < pc) {
        gges_cfggp_crossover(mother, father, daughter, son, max_depth, node_sel, rnd);
        return false;
    } else {
        gges_cfggp_reproduction(mother, daughter);
        gges_cfggp_reproduction(father, son);

        if (p < (pm + pc)) {
            gges_cfggp_mutation(g, daughter, pm, mut_depth, max_depth, node_sel, rnd);
            gges_cfggp_mutation(g, son, pm, mut_depth, max_depth, node_sel, rnd);

            return false;
        }

        return true;
    }
}








/*******************************************************************************
 * internal helper function implementations
 ******************************************************************************/
static struct gges_cfggp_node *create_node(struct gges_bnf_production *p)
{
    int i;
    struct gges_cfggp_node *node;

    node = ALLOC(1, sizeof(struct gges_cfggp_node), false);

    node->parent = NULL;

    node->p = p;

    node->depth = 0; /* this will be calculated once the tree is
                      * complete */

    node->size = 1;  /* this will be calculated properly once the tree
                      * is complete */

    node->num_nt = 0;
    for (i = 0; i < p->size; ++i) {
        if (!p->tokens[i].terminal) node->num_nt++;
    }

    node->children = ALLOC(node->num_nt, sizeof(struct gges_cfggp_node *), false);
    for (i = 0; i < node->num_nt; ++i) node->children[i] = NULL;

    node->data_fields = ALLOC(p->size, sizeof(char *), false);
    for (i = 0; i < p->size; ++i) node->data_fields[i] = NULL;

    return node;
}



static struct gges_cfggp_node *replicate_tree(struct gges_cfggp_node *t)
{
    int i;
    struct gges_cfggp_node *dest;

    dest = create_node(t->p);

    dest->depth = t->depth;
    dest->size = t->size;

    for (i = 0; i < dest->num_nt; ++i) {
        dest->children[i] = replicate_tree(t->children[i]);
        dest->children[i]->parent = dest;
    }

    for (i = 0; i < t->p->size; ++i) {
        if (t->data_fields[i]) {
            dest->data_fields[i] = ALLOC((strlen(t->data_fields[i]) + 1), sizeof(char), false);
            if (dest->data_fields[i] == NULL) {
                fprintf(stderr, "%s:%d - ERROR: Failed to allocate memory\n",
                        __FILE__, __LINE__);
                exit(EXIT_FAILURE);
            }
            strcpy(dest->data_fields[i], t->data_fields[i]);
        }
    }

    return dest;
}



static void map_sequence(struct gges_mapping *m,
                         struct gges_cfggp_node *t)
{
    int i, j;

    if (t == NULL) return;

    j = 0;
    for (i = 0; i < t->p->size; ++i) {
        if (t->p->tokens[i].terminal) {
            /* current token is a terminal, and needs to be printed
             * into the destination stream */
               
            if (t->p->tokens[i].data_field) {
                gges_mapping_append_symbol(m, t->data_fields[i]);
                gges_mapping_append_symbol(m, " ");
            } else {
                gges_mapping_append_symbol(m, t->p->tokens[i].symbol);
                gges_mapping_append_symbol(m, " ");
            }
        } else {
            /* the current token is a non-terminal, and so needs
             * further expansion. We do this via a recursive call to
             * the relevant production of the corresponding
             * non-terminal */
            map_sequence(m, t->children[j++]);
        }

    }
}



static struct gges_derivation_tree *map_derivation(
    struct gges_cfggp_node *t)
{
    int i, c;
    struct gges_derivation_tree *dt, *sub;

    dt = gges_create_derivation_tree(t->p->size);
    dt->label = ALLOC(strlen(t->p->nt->label) + 1, sizeof(char), false);
    strcpy(dt->label, t->p->nt->label);

    c = 0;
    for (i = 0; i < t->p->size; ++i) {
        if (t->p->tokens[i].terminal) {
            sub = gges_create_derivation_tree(0);
            if (t->p->tokens[i].data_field) {
                sub->label = ALLOC((strlen(t->data_fields[i]) + 1), sizeof(char), false);
                strcpy(sub->label, t->data_fields[i]);
            } else {
                sub->label = ALLOC(strlen(t->p->tokens[i].symbol) + 1, sizeof(char), false);
                if (sub->label == NULL) {
                    fprintf(stderr, "%s:%d - ERROR: Failed to allocate memory\n",
                            __FILE__, __LINE__);
                    exit(EXIT_FAILURE);
                }
                strcpy(sub->label, t->p->tokens[i].symbol);
            }
        } else {
            sub = map_derivation(t->children[c++]);
        }
        gges_add_sub_derivation(dt, sub);
    }

    return dt;
}



static void calculate_depths(struct gges_cfggp_node *t)
{
    int i;

    t->depth = 1;
    t->size = 1;
    for (i = 0; i < t->num_nt; ++i) {
        calculate_depths(t->children[i]);
        if ((t->children[i]->depth + 1) > t->depth) {
            t->depth = t->children[i]->depth + 1;
        }

        t->size += t->children[i]->size;
    }
}

/**
 * 
 * @param p - the production to process
 * @param rnd - a pseudo aleatory number, that could be an integer or a real number
 * @return a producton with the terminal RANDINT(min, max) replaced by a integer
 *         number between min and max 
 *          OR 
 *          a producton with the terminal RANDFLOAT(min, max) replaced by a real
 *          number between min and max 
 */
static struct gges_bnf_production *random_number(struct gges_bnf_production *p,
                                                double (*rnd)(void), char *tag) {

    int len_substr, minInt, maxInt, randInt;
    double minDouble, maxDouble, randDouble;
    char *strRand = NULL;
    char *maxstr = "";
    char *substr = "";


    
    if(strcmp(tag, "integer")==0){
        //Define the interval to apply the rand considering the terminal RANDINT(min, max)
        len_substr = strlen(p->tokens->symbol) - 9;    
        substr = (char*) malloc(sizeof (char)*len_substr + 1);
        strcpy(substr, "");
        strncpy(substr, p->tokens->symbol + 8, len_substr);
        substr[len_substr] = '\0';
        
        
        //Set the max and the min given the rand string:
        minInt = atoi(strtok(substr, ","));
        maxstr = strtok(NULL, ","); 
        maxInt = atoi(maxstr);
    
        //Generate the rand of a integer considering a predefined interval:
        randInt = (maxInt - minInt + 1)*(rnd()) + minInt;
        strRand = (char*) malloc(sizeof (char)*strlen(maxstr) + 1);
        sprintf(strRand, "%d", randInt);
        
    }else if(strcmp(tag, "float")==0){
        //Define the interval to apply the rand considering the terminal RANDFLOAT(min, max)
        len_substr = strlen(p->tokens->symbol) - 11;    
        substr = (char*) malloc(sizeof (char)*len_substr + 1);
        strcpy(substr, "");
        strncpy(substr, p->tokens->symbol + 10, len_substr);
        substr[len_substr] = '\0';
        
        //Set the max and the min given the rand string:
        minDouble = atof(strtok(substr, ","));
        maxstr = strtok(NULL, ","); 
        maxDouble = atof(maxstr);
    
        //Generate the rand of a integer considering a predefined interval:
        randDouble = (maxDouble - minDouble)*(rnd()) + minDouble;
        strRand = (char*) malloc(sizeof (char)*strlen(maxstr) + 1);
        sprintf(strRand, "%f", randDouble);
    }


    //Create a struct gges_bnf_production to save the token::
    struct gges_bnf_token *tk = (struct gges_bnf_token*) malloc(sizeof (struct gges_bnf_token));
    tk->terminal = p->tokens->terminal;
    tk->data_field = p->tokens->data_field;
    tk->nt = p->tokens->nt;
    tk->symbol = (char*) malloc(sizeof (char)*(strlen(strRand) + 1));
    //Save the generated rand in the interval in the tk->symbol, 
    //  which is the symbol of this terminal:
    sprintf(tk->symbol, "%s", strRand);

    //Create a struct gges_bnf_production to save the production:
    struct gges_bnf_production *prd = (struct gges_bnf_production*) malloc(sizeof (struct gges_bnf_production));
    prd->id = p->id;
    prd->size = p->size;
    prd->tokens = tk;
    prd->recursive = p->recursive;
    prd->nt = p->nt;
    prd->min_depth = p->min_depth;

       
  return prd;
} 


static bool sensible_init(struct gges_bnf_grammar *g,
                          struct gges_cfggp_node **t,
                          struct gges_bnf_non_terminal *nt,
                          int depth, int min_depth, int max_depth,
                          double (*rnd)(void))
{
    int i, c, np, reqd;
    struct gges_bnf_production **choices, *p;
    p = ALLOC(nt->size, sizeof(struct gges_bnf_production), false);;
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

        *t = NULL;
    } else {
        /* pick one of the available productions at random */

        p = choices[(int)(rnd() * np)];
        //free(choices);


        if((p->tokens->terminal)){
          if(strstr(p->tokens->symbol, "RANDINT")!=NULL){  
            p = random_number(p, rnd, "integer");
           
          }else if(strstr(p->tokens->symbol, "RANDFLOAT")!=NULL){  
            p = random_number(p, rnd, "float");          
          }
        }

        *t = create_node(p);          

         
        /* now that we have a valid production, scan through all its
         * tokens, and for any non-terminals, recursively call the
         * sensible init function from this point */
        success = true;
        c = 0;
                   
        for (i = 0; i < p->size; ++i) {
          if(strcmp(p->tokens[i].symbol, " ")!=0){
            if (p->tokens[i].terminal) {                 
                if (p->tokens[i].data_field) {

                    (*t)->data_fields[i] = gges_bnf_init_data_field(g, (*t)->p->tokens[i].symbol, rnd);
                }
                continue;
            }
            success = sensible_init(g, (*t)->children + c,
                                    p->tokens[i].nt,
                                    depth + 1, min_depth, max_depth,
                                    rnd);
            if (!success){ 
            	break;
            }

            (*t)->children[c++]->parent = *t;
          }
        }
    }


    return success;
            

}


/* recursively scans a tree and sums the depths of all the subtrees
 * that match the required "type" (i.e., non-terminal of the
 * grammar). If no specific type is required, then the required type
 * should be NULL */
static double sum_tree_vals(struct gges_cfggp_node *t,
                         struct gges_bnf_non_terminal *required_type,
                         enum gges_cfggp_node_selection node_sel)
{
    int i;
    double sum;

    if ((required_type == NULL) || (t->p->nt == required_type)) {
        switch (node_sel) {
        case PICK_NODE_UNIFORM_RANDOM: default: sum = 1; break;
        case PICK_NODE_KOZA_90_10: sum = ((t->depth == 1) ? 0.10 : 0.90); break;
        case PICK_NODE_DEPTH_PROP: sum = t->depth; break;
        }
    } else {
        sum = 0.0;
    }

    for (i = 0; i < t->num_nt; ++i) {
        sum += sum_tree_vals(t->children[i], required_type, node_sel);
    }

    return sum;
}

/* recursively scans the tree to find the subtree that matches the
 * required non-terminal label, and was selected in the roulette wheel
 * process (proportional to subtree depth) */
static struct gges_cfggp_node *locate_subtree(
    struct gges_cfggp_node *t,
    struct gges_bnf_non_terminal *required_type,
    enum gges_cfggp_node_selection node_sel,
    double *remaining_sum)
{
    struct gges_cfggp_node *s;
    int i;

    if ((required_type == NULL) || (t->p->nt == required_type)) {
        switch (node_sel) {
        case PICK_NODE_UNIFORM_RANDOM: default: *remaining_sum -= 1; break;
        case PICK_NODE_KOZA_90_10: *remaining_sum -= ((t->depth == 1) ? 0.10 : 0.90); break;
        case PICK_NODE_DEPTH_PROP: *remaining_sum -= t->depth; break;
        }

        /* if the remaining depth is wiped out, then we have
         * identified the node that we want to select */
        if (*remaining_sum <= 0) return t;
    }

    /* if we reach here, then the required node was not identified,
     * and therefore we need to descend into the current tree's
     * children */
    for (i = 0; i < t->num_nt; ++i) {
        s = locate_subtree(t->children[i], required_type, node_sel, remaining_sum);

        /* if the recursive search of the subtree identified the
         * subtree, then we do not need to proceed with the search any
         * further, and should just return the identified tree */
        if (s != NULL) return s;
    }

    /* if we get here, then the required node was not in any of the
     * current node's subtrees. This is not an error, but flag the
     * return as NULL to reflect the failure to find the required
     * node */
    return NULL;
}

/* selects a subtree in the given tree in a roulette wheel like
 * process where the probability of selection of a subtree is
 * proportional to its depth */
static int pick_subtree(struct gges_cfggp_node **pick,
                        struct gges_cfggp_node *parent,
                        struct gges_bnf_non_terminal *required_type,
                        enum gges_cfggp_node_selection node_sel,
                        double (*rnd)(void))
{
    int i;
    double node_sum;

    node_sum = sum_tree_vals(parent, required_type, node_sel);
    if (node_sum == 0) {
        /* no subtrees of the required type exist in the tree */
        *pick = NULL;

        return -1;
    }

    /* pick a random point in the tree proportional to depth, and then
     * perform the search for the node */
    node_sum = (rnd() * node_sum);
    *pick = locate_subtree(parent, required_type, node_sel, &node_sum);

    if (*pick == NULL) {
        /* could not find a suitable subtree in the parent */
        fprintf(stderr, "%s%d - WARNING! Could not pick subtree\n",
                __FILE__, __LINE__);
        return -1;
    } else if ((*pick)->parent == NULL) {
        /* we picked the root of the tree */
        return -1;
    } else {
        /* find the index of the chosen subtree within its parent */
        for (i = 0; i < (*pick)->parent->num_nt; ++i) {
            if (*pick == (*pick)->parent->children[i]) return i;
        }

        /* should not get here unless something has gone wrong */
        fprintf(stderr, "%s%d - WARNING! Could not pick subtree\n",
                __FILE__, __LINE__);
        return -1;
    }
}



static struct gges_cfggp_node *perform_tree_swap(struct gges_cfggp_node **tree,
                                                 struct gges_cfggp_node *pick,
                                                 int pick_idx,
                                                 struct gges_cfggp_node *rep)
{
    struct gges_cfggp_node *parent;
    if (pick == *tree) {
        /* we're crossing at the root, so replace the root and return it */
        *tree = rep;
        return pick;
    } else {
        parent = pick->parent;

        parent->children[pick_idx] = rep;
        pick->parent = rep->parent;
        rep->parent = parent;

        return pick;
    }
}
