/* Interface for Bit2 */
/* Benjamin deButts (bdebut01) & Samuel Duncan (sdunca01) */

#include <bit.h>
#include <stdlib.h>
#include <assert.h>

#define T Bit2_T
typedef struct T *T;
struct T {
        unsigned height;
        unsigned width;
        Bit_T arr;
};

/*  creates an instance of the 2D Bit array height high and width wide. */
extern T Bit2_new(int height, int width);

/* frees up the memory allocated for the array */
extern void Bit2_free(T array);

/* returns the total number of spaces in the array (height * width). */
extern int Bit2_length(T array);

/* returns the number of ones in the array */
extern int Bit2_count(T array);

/* returns the value ( 1 or 0 ) located at the passed height width pair.*/
extern int Bit2_get(T array, int col, int row);

/*
* changes the value stored at the passed height-width location to the bit
* value passed. Returns the location's previous value.
*/
extern int Bit2_put(T array, int col, int row, int bit);

/* 
* calls "apply" function on every bit in the array, moving left to right and
* then down
*/
extern void Bit2_map_row_major(T array,
                void apply(int col, int row, int bit, void *cl), void *cl);

/*
* calls "apply" function on every bit in the array, moving down each column and
* then across.
*/
extern void Bit2_map_col_major(T array,
                void apply(int col, int row, int bit, void *cl), void *cl);


#undef T