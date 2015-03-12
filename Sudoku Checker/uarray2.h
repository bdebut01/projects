/* Interface for UArray2 */
/* Benjamin deButts (bdebut01) & Samuel Duncan (sdunca01) */

#include <uarray.h>
#include <stdlib.h>
#include <assert.h>

#define T UArray2_T
typedef struct T *T;
struct T {
        unsigned int height;
        unsigned int width;
        UArray_T arr; /* Hanson 1D array */
};

/* function creates an instance of the 2D array */
extern T UArray2_new(int height, int width, int size);

/* frees up the memory where the passed array is located */
extern void UArray2_free(T array);

/* function will return the total number of slots to store variables */
extern unsigned int UArray2_length(T array);

/* function returns the size (in bytes) of a element stored */
extern unsigned int UArray2_size(T array);

/*
* function returns a pointer to the element stored in the passed location 
* (row, col).
*/
extern void *UArray2_at(T array, int col, int row);

/* 
* for every element in the array, calls the passed "apply" function.
* The row_major version of the function proceeds left to right across each row,
* then moves to the next row.
*/
extern void UArray2_map_row_major(T array,
                                  void apply(int col, int row, void *value,
                                              void *cl), void *cl);

/* 
* for every element in the array, calls the passed "apply" function.
* The col_major version of the function proceeds top to bottom down
* each col, then moves to the column.
*/
extern void UArray2_map_col_major(T array,
                                  void apply(int col, int row, void *value,
                                              void *cl), void *cl);
#undef T                    