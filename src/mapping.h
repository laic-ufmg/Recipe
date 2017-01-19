#ifndef GGES_MAPPING
#define GGES_MAPPING

#ifdef __cplusplus
extern "C" {
#endif

    struct gges_mapping {
        /* the expressed source code of the individual with respect to
         * the supplied grammar */
        char *buffer;
        int l; /* the length of the string in the buffer */
        size_t sz; /* size of the buffer used for the mapping */
    };

    void gges_mapping_append_symbol(struct gges_mapping *mapping, char *token);

#ifdef __cplusplus
}
#endif

#endif
