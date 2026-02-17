#include <stdio.h>
#include "Image.h"
#include <stdlib.h>

// get the R intensity of pixel (x, y) in image //
unsigned char GetPixelR(const Image *image, unsigned int x, unsigned int y){
    // check bounds //       
    if (x < image->W && y < image->H){
        // unidimensional index calculation for tuple coordinates //
        unsigned int idx = x + y * image->W;
        return image->R[idx];
    }
    // return 0 if coordinates are not within bounds //
    else{
        return 0;
    }
}

// get the G intensity of pixel (x, y) in image //
unsigned char GetPixelG(const Image *image, unsigned int x, unsigned int y){
    // check bounds //       
    if (x < image->W && y < image->H){
        // unidimensional index calculation for tuple coordinates //
        unsigned int idx = x + y * image->W;
        return image->G[idx];
    }
    // return 0 if coordinates are not within bounds //
    else{
        return 0;
    }
}

// get the B intensity of pixel (x, y) in image //
unsigned char GetPixelB(const Image *image, unsigned int x, unsigned int y){
    // check bounds //       
    if (x < image->W && y < image->H){
        // unidimensional index calculation for tuple coordinates //
        unsigned int idx = x + y * image->W;
        return image->B[idx];
    }
    // return 0 if coordinates are not within bounds //
    else{
        return 0;
    }
}

// set the R intensity of pixel (x, y) in image to r//
void SetPixelR(Image *image, unsigned int x, unsigned int y, unsigned char r){
    // bounds check //
    if (x < image->W && y < image->H){
        // calculate unidimensional index that corresponds to (x, y) //
        unsigned int idx = x + y * image->W;
        // set pixel (x,y) to color intensity //
        image->R[idx] = r;
    }
}

// set the G intensity of pixel (x, y) in image to g//
void SetPixelG(Image *image, unsigned int x, unsigned int y, unsigned char g){
    // bounds check //
    if (x < image->W && y < image->H){
        // calculate unidimensional index that corresponds to (x, y) //
        unsigned int idx = x + y * image->W;
        // set pixel (x,y) to color intensity //
        image->G[idx] = g;
    }
}

// set the B intensity of pixel (x, y) in image to b //
void SetPixelB(Image *image, unsigned int x, unsigned int y, unsigned char b){
    // bounds check //
    if (x < image->W && y < image->H){
        // calculate unidimensional index that corresponds to (x, y) //
        unsigned int idx = x + y * image->W;
        // set pixel (x,y) to color intensity //
        image->B[idx] = b;
    }
}

unsigned int ImageWidth(const Image *image){
    // get constant value for image width //
    unsigned int width = image->W;
    return width;
}

unsigned int ImageHeight(const Image *image){
    // get constant value for image height //
    unsigned int height = image->H;
    return height;
}

Image *CreateImage(unsigned int Width, unsigned int Height){

    Image *image = (Image *)malloc(sizeof(Image)); // creates pointer 'image' for Image structure //
    if (!image) return NULL; // allocation failure check //

    // sets the width(W) and height(H) within the Image structure //
    image->W = Width;
    image->H = Height;

    // allocate color channel arrays with (Width * Height) many elements of size (unsigned char) for R, G, and B//
    image->R = (unsigned char *)calloc(Width * Height, sizeof(unsigned char));
    image->G = (unsigned char *)calloc(Width * Height, sizeof(unsigned char));
    image->B = (unsigned char *)calloc(Width * Height, sizeof(unsigned char));

    if (!image->R || !image->G || !image->B){ // allocation failure check //
        free(image->R);
        free(image->G);
        free(image->B);
        free(image);
        return NULL;
    }
   
    return image;
}

void DeleteImage(Image *image){
    if (!image) return;
    // deallocate memory for each color channel //
    free(image->R);
    free(image->G);
    free(image->B);
   
    // deallocate image memory from Image structure // 
    free(image);
}
//EOF//
