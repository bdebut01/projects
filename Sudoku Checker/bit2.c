/*
*       Implementation for bit2.h
*       by Benjamin deButts (bdebut01) & Samuel Duncan (sdunca01)
*       Comp 40, HW2, PART B
*
*       Uses Hanson Bit Vectors to create a 2D array of bits. 
*/

#include "bit2.h"
#define T Bit2_T

void initialize_Bit2(T array, int height, int width);
unsigned int locate_index(int col, int row, int width);
void checkboundaries(int height, int width, int col, int row);

/* Can't pass a height or width of 0 */
T Bit2_new (int height, int width)
{
        unsigned int length = height * width;
        T bit_arr = malloc(sizeof(*bit_arr));
        if (length > 0) {
                /* Create 1D Hanson Bit Vector */
                bit_arr->arr = Bit_new(length);
                /* Put height and width into a Bit2_T struct */
                initialize_Bit2(bit_arr, height, width);
        }
        else {
                exit(EXIT_FAILURE); /* Correct error output? */
        }
        return bit_arr;
}

/* assigns height and width to Bit2_T*/
void initialize_Bit2(T array, int height, int width)
{
        assert(array != NULL); /* Not out of memory */
        array->height = height;
        array->width = width;
}

void Bit2_free(T array)
{
        assert(array != NULL);
        /* Free member Hanson Bit Vector */
        Bit_free(&(array->arr));
        free(array);
}

int Bit2_length(T array)
{
        return (array->height * array->width);
}

int Bit2_count(T array)
{
        return Bit_count(array->arr);
}

int Bit2_get(T array, int col, int row)
{
        checkboundaries(array->height, array->width, col, row);
        return Bit_get(array->arr, locate_index(col, row, array->width));
}

int Bit2_put(T array, int col, int row, int bit)
{
        checkboundaries(array->height, array->width, col, row);
        return Bit_put(array->arr, locate_index(col, row, array->width), bit);
}

/* 
* Function asserts that desired index is within the boundaries of the array.
*/
void checkboundaries(int height, int width, int col, int row)
{
        /* Too big a coordinate? */
        assert(col < width && row < height);

        /* Too small a coordinate/impossible */
        assert(row >= 0 && col >= 0);
}

/*
* Function computes where within the one-dimensional uarray the pair of 
* coordinates would be. Returns this single int (index).
*/
unsigned int locate_index(int col, int row, int width)
{
        return ((row * width) + col);
}

/*
* Note: any apply function that wants to change the data, must call "put"...
* Because bits are not passed as pointers.
*/
void Bit2_map_row_major(T array,
                void apply(int col, int row, int bit, void *cl), void *cl)
{
        assert(array != NULL);
        assert(apply != NULL);
        unsigned int i; /* i == row */
        unsigned int j; /* j == col */
        for (i = 0; i < array->height; i++) {
                for (j = 0; j < array->width; j++) {
                        apply(j, i, Bit2_get(array, j, i), cl);
                }
        }  
}

/*
* Note: any apply function that wants to change the data, must call "put"...
* Because bits are not passed as pointers.
*/
void Bit2_map_col_major(T array,
                void apply(int col, int row, int bit, void *cl), void *cl)
{
        assert(array != NULL);
        assert(apply != NULL);
        unsigned int i; /* i == row */
        unsigned int j; /* j == col */
        for (j = 0; j < array->width; j++) {
                for (i = 0; i < array->height; i++) {
                        apply(j, i, Bit2_get(array, j, i), cl);
                }
        }
}

#undef T