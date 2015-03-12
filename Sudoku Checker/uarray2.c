/*
*       Implementation for uarray2.h
*       by Benjamin deButts (bdebut01) & Samuel Duncan (sdunca01)
*       Comp 40, HW2, PART A
*
*       Uses Hanson unboxed arrays to create 2D unboxed arrays.
*/
#include "uarray2.h"
#define T UArray2_T

void initialize_UArray2(T array, int height, int width);
unsigned int locate_1D_index(int col, int row, int width);
void checkboundaries(int height, int width, int col, int row);

T UArray2_new(int height, int width, int size)
{
        unsigned int length = height * width;
        T UArray2 = malloc(sizeof(*UArray2));
        if(length > 0) {
                /* Create 1D Hanson UArray */
                UArray2->arr = UArray_new(length, size);
                /* Put width and height into UArray_T struct */
                initialize_UArray2(UArray2, height, width);
        }
        else {
                exit(EXIT_FAILURE);
        }
        return UArray2;
}

/* Put width and height into UArray_T struct */
void initialize_UArray2(T array, int height, int width)
{
        assert(array != NULL); /* Not out of memory */
        array->height = height;
        array->width = width;
}

void UArray2_free(T array)
{
        assert(array != NULL);
        /* Free member Hanson UArray */
        UArray_free(&(array->arr));
        free(array);
}

unsigned int UArray2_length(T array)
{
        /* Total spaces for elements, width * height */
        return (array->height * array->width);
}

unsigned int UArray2_size(T array)
{
        return UArray_size(array->arr);
}

void *UArray2_at(T array, int col, int row)
{
        unsigned int arr_width = array->width;
        unsigned int arr_height = array->height;
        
        checkboundaries(arr_height, arr_width, col, row);
        /* Within boundaries, proceed to access & return value at index */
        return UArray_at(array->arr, locate_1D_index(col, row, arr_width));
}

/*
* Function computes where within the one-dimensional uarray the pair of 
* coordinates would be. Returns this single int (index).
*/
unsigned int locate_1D_index(int col, int row, int width)
{
        return ((row * width) + col);
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
* Function calls the passed apply function on each index in the array.
* Also, asserts that both the array and the apply function exist.
*/
void UArray2_map_row_major(T array, void apply(int col, int row, void *value,
                                void *cl), void *cl)
{
        assert(array != NULL);
        assert(apply != NULL);
        unsigned int i; /* i == row */
        unsigned int j; /* j == col */
        for(i = 0; i < array->height; i++) {
                for(j = 0; j < array->width; j++) {
                        apply(j, i, UArray2_at(array, j, i), cl);
                }
        }
}

/*
* Function calls the passed apply function on each index in the array.
* Also, asserts that both the array and the apply function exist.
*/
void UArray2_map_col_major(T array, void apply(int col, int row, void *value,
                                void *cl), void *cl)
{
        assert(array != NULL);
        assert(apply != NULL);
        unsigned int i; /* i == row */
        unsigned int j; /* j == col */
        for(j = 0; j < array->width; j++) {
                for(i = 0; i < array->height; i++) {
                        apply(j, i, UArray2_at(array, j, i), cl);
                }
        }
}

#undef T  