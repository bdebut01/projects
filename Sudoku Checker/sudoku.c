/*      
*       sudoku.c
*       
*       Samuel Duncan (sdunca01) & Benjamin deButts (bdebut01)
*
*       Program reads in a sudoku from either standard input or from a file.
*       If the input is a correct sudoku, the program will exit(0).
*       Otherwise, exit(1).
*/
#include "uarray2.h"
#include <pnmrdr.h>
#include <stdio.h>

struct DataPackage {
        UArray2_T puzzle_arr;
        UArray2_T row_counts;
        UArray2_T col_counts;
        UArray2_T box_counts;
        Pnmrdr_T image;
        FILE* fp;
};

void sudoku(FILE *fp);
Pnmrdr_T checkImageFormat(FILE *fp);
void read_puzzle(Pnmrdr_T image, FILE *fp);
void populate_counters(int col, int row, void *value, void *cl);
void setzeroes(int col, int row, void *value, void *cl);
void increment_Counts(UArray2_T *array, int line, int value);
unsigned int find_box_num(int col, int row);

/* Checking Functions */
void check_Counts(struct DataPackage data);
void check_ones(int col, int row, void* value, void *cl);

/* Freeing Function */
void free_data(struct DataPackage *data);

const unsigned int SUDOKU_DIM = 9;
const unsigned int DENOM = 9;

int main(int argc, char *argv[])
{
        if(argc == 1) {
                sudoku(stdin);
        } else {
                if(argc == 2) {
                        FILE *fp = fopen(argv[1], "rb");
                        if(fp == NULL) {
                                exit(1);
                        }
                        sudoku(fp);
                } else { /*too many files */
                        exit(1);
                }
        }
}

void sudoku(FILE *fp)
{
        /* Check file format and convert to Pnmrdr_T */
        Pnmrdr_T image = checkImageFormat(fp);
        /* File fulfills all formatting conditions, read in input */
        read_puzzle(image, fp);
}

/* 
* Function checks to ensure compatible image type and errors otherwise. 
*/
Pnmrdr_T checkImageFormat(FILE *fp)
{
        Pnmrdr_T image = NULL;
        TRY
                image = Pnmrdr_new(fp);
        /* Bad format? */
        EXCEPT(Pnmrdr_Badformat)
                fclose(fp);
                Pnmrdr_free(&image);
                exit(1);
        END_TRY;
        /* Out of memory? */
        if(image == NULL) {
                fclose(fp);
                exit(1);
        }
        Pnmrdr_mapdata map = Pnmrdr_data(image);
        /* 
        * In order, "if" ensures:
        * image is grayscale, width and height are standard sudoku dimensions, 
        * and finallly that the image's denominator is appropriate.
        */
        if((map.type == Pnmrdr_gray) && (map.width == SUDOKU_DIM) &&
           (map.height == SUDOKU_DIM) && (map.denominator == DENOM)) {
                return image;
        }
        /* Otherwise, close, free, and exit  */
        fclose(fp);
        Pnmrdr_free(&image);
        exit(1);
}

void read_puzzle(Pnmrdr_T image, FILE *fp)
{
        struct DataPackage data;
        /* Create all counter arrays */
        data.row_counts = UArray2_new(SUDOKU_DIM, SUDOKU_DIM, sizeof(int));
        data.col_counts = UArray2_new(SUDOKU_DIM, SUDOKU_DIM, sizeof(int));
        data.box_counts = UArray2_new(SUDOKU_DIM, SUDOKU_DIM, sizeof(int));
        /* Create puzzle array */
        data.puzzle_arr = UArray2_new(SUDOKU_DIM, SUDOKU_DIM, sizeof(int));
        
        /* Put file into Data Package so it can be closed upon exit */
        data.fp = fp;
        
        /* Initialize all counter arrays */
        UArray2_map_row_major(data.row_counts, setzeroes, NULL);
        UArray2_map_row_major(data.col_counts, setzeroes, NULL);
        UArray2_map_row_major(data.box_counts, setzeroes, NULL);
        data.image = image;
        /* Map on every index in the sudoku 2D array */
        UArray2_map_row_major(data.puzzle_arr, populate_counters, &data);
        
        /* Look at counter arrays, ensure all counts are equal 1 */
        check_Counts(data);
        free_data(&data);
}

/* Sets all elements of a UArray2 to 0 */
void setzeroes(int col, int row, void *value, void *cl)
{
        (void)col;
        (void)row;
        (void)cl;
        *(unsigned int*)value = 0;
}

/*
* There are three 2D arrays of counters that are incremented as values are read.
* For each value that is read:
*       the row_counts array will increment at (row, value)
*       the col_counts array will increment at (col, value)
*       the function will find the correct 3x3 "box" associated with the 
*               value's coordinates, and
*       the box_counts array will increment at (box_num, value)
* If the file is a correct sudoku solution, all the elements of those arrays
*       will hold a value of 1 when all data has been read.
*/
void populate_counters(int col, int row, void *value, void *cl)
{
        struct DataPackage *data = (struct DataPackage*)cl;
        /* "value" given the int in the sudoku input */
        TRY
                *(unsigned int*)value = Pnmrdr_get(data->image);
        EXCEPT(Pnmrdr_Badformat)
                free_data(data);
                exit(1);
        END_TRY;
        unsigned int val = *(unsigned int *)value;
        /* Ensure value is inbounds */
        if(val < 1 || val > DENOM) {
                free_data(data);
                exit(1);
        }
        
        int box_num = find_box_num(col, row);
        /* Update row/col/box counter arrays */
        increment_Counts(&(data->row_counts), row, val);
        increment_Counts(&(data->col_counts), col, val);
        increment_Counts(&(data->box_counts), box_num, val);
}

/* 
* Called when mapping, the function increments at the passed array's line (row)
* and value (col). 
*/
void increment_Counts(UArray2_T *array, int line, int value)
{
        unsigned int *index_val = NULL;
        index_val = UArray2_at(*array, (value - 1), line);
        (*index_val)++;
}

/* 
* the function will find the correct 3x3 "box" associated with the passed 
* coordinates (col/row).
*/
unsigned int find_box_num(int col, int row)
{
        return ((3 * (row / 3)) + (col / 3));
}

/************************** CHECKING ******************************************/

void check_Counts(struct DataPackage data)
{
        /* Map & Check each counter array */
        UArray2_map_row_major(data.row_counts, check_ones, &data);
        UArray2_map_row_major(data.col_counts, check_ones, &data);
        UArray2_map_row_major(data.box_counts, check_ones, &data);
}

void check_ones(int col, int row, void* value, void *cl)
{
        (void)col;
        (void)row;
        /* 
        * If ever run into anything but a 1, exit(1) because the counter should 
        * be "one" in a correct solution.
        */
        if(*(unsigned int*)value != 1) {
                free_data(cl);
                exit(1);
        }
}

void free_data(struct DataPackage *data)
{
        UArray2_free(data->puzzle_arr);
        UArray2_free(data->row_counts);
        UArray2_free(data->col_counts);
        UArray2_free(data->box_counts);
        
        fclose(data->fp);
        
        Pnmrdr_free(&(data->image));
}
