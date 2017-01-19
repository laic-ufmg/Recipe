#ifndef _PARAMETERS_H
#define	_PARAMETERS_H

#ifdef	__cplusplus
extern "C" {
#endif

    #include "gges.h"

    void process_parameter(char *param, struct gges_parameters *params);
    void parse_parameters(char *params_file, struct gges_parameters *params);

#ifdef	__cplusplus
}
#endif

#endif	/* _PARAMETERS_H */
