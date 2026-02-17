#ifndef DIPS_H
#define DIPS_H
#include "Constants.h"

/* change a color image to black & white */
void BlackNWhite(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
         unsigned char B[WIDTH][HEIGHT]);

/* reverse image color */
void Negative(unsigned char R[WIDTH][HEIGHT],
          unsigned char G[WIDTH][HEIGHT],
          unsigned char B[WIDTH][HEIGHT]);

/* color filter */
void ColorFilter(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
                 unsigned char B[WIDTH][HEIGHT],
         int target_r, int target_g, int target_b, int threshold,
         int replace_r, int replace_g, int replace_b);

/* edge detection */
void Edge(unsigned char R[WIDTH][HEIGHT],
      unsigned char G[WIDTH][HEIGHT],
          unsigned char B[WIDTH][HEIGHT]);

/* mirror image horizontally */
void HMirror(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
             unsigned char B[WIDTH][HEIGHT]);

/* shuffle the image */
void Shuffle(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
             unsigned char B[WIDTH][HEIGHT]);


/* add border */
void AddBorder(unsigned char R[WIDTH][HEIGHT],
           unsigned char G[WIDTH][HEIGHT],
               unsigned char B[WIDTH][HEIGHT],
           char color[SLEN], int border_width);

/* flip image vertically */
void VFlip(unsigned char R[WIDTH][HEIGHT],
       unsigned char G[WIDTH][HEIGHT],
           unsigned char B[WIDTH][HEIGHT]);

/* pixelate image */
void Pixelate(unsigned char R[WIDTH][HEIGHT],
           unsigned char G[WIDTH][HEIGHT],
               unsigned char B[WIDTH][HEIGHT],
               int block_size);

#endif
