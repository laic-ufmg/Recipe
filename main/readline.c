#include <stdio.h>
#include <stdlib.h>

#include <ctype.h>  /* needed for isspace */
#include <string.h> /* needed for string manipulation (e.g., strlen) */

static int readline(char **lineptr, size_t *n, FILE *stream)
{
    char *bufptr;
    char *p;
    size_t size;
    int c;

    if (lineptr == NULL) return -1;
    if (stream == NULL) return -1;
    if (n == NULL) return -1;

    p = bufptr = *lineptr;
    size = *n;

    c = fgetc(stream);
    if (c == EOF) return -1;

    if (bufptr == NULL) {
    	bufptr = malloc(BUFSIZ);
    	if (bufptr == NULL) {
            fprintf(stderr, "%s:%d - Could not allocate memory for buffer.\n", __FILE__, __LINE__);
    		return -1;
    	}
    	size = BUFSIZ;
    }
    p = bufptr;
    while(c != EOF) {
    	if ((p - bufptr) > (size - 1)) {
    		size += BUFSIZ;
    		bufptr = realloc(bufptr, size);
    		if (bufptr == NULL) {
                fprintf(stderr, "%s:%d - Could not reallocate memory for buffer.\n", __FILE__, __LINE__);
    			return -1;
    		}
    	}
    	*p++ = c;
    	if (c == '\n') {
    		break;
    	}
    	c = fgetc(stream);
    }

    *p++ = '\0';
    *lineptr = bufptr;
    *n = size;

    return p - bufptr - 1;
}

char *trim(char *str)
{
    char *end;

    if (strlen(str) > 0) {
        while (isspace(*str)) str++;

        end = str + strlen(str) - 1;
        while (end > str && isspace(*end)) end--;

        *(end + 1) = '\0';
    }

    return str;
}

char *next_line(char **buffer, size_t *sz, FILE *data)
{
    char *line;
    readline(buffer, sz, data);

    line = *buffer;
    if (strlen(line) > 0) {
        line[strcspn(*buffer, "\n")] = '\0'; /* chomp newline character, if present */
        line[strcspn(*buffer, "#")] = '\0';  /* chomp comments at end of line */
    }

    return trim(line);
}
