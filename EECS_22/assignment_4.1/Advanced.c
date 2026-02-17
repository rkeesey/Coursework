#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "DIPs.h"
#include "FileIO.h"
#include "Advanced.h"
#include "Constants.h"
#include <math.h>

/* Crop */
Image *Crop(Image *image, int x, int y, int W, int H){
    
    const char *fname = "crop";
    
    unsigned int width = ImageWidth(image);
    unsigned int height = ImageHeight(image);

    Image *cropped = CreateImage(W, H);

    for (int j = y; j < H + y; j++)
    {
        for (int i = x; i < W + x; i++)
        {   if (i > width){
                i = width;
            }
            if (j > height){
                j = height;
            }
            unsigned char temp_1 = GetPixelR(image, i, j);
            SetPixelR(cropped, i - x, j - y, temp_1);

            temp_1 = GetPixelG(image, i, j);
            SetPixelG(cropped, i - x, j - y, temp_1);
            
            temp_1 = GetPixelB(image, i, j);
            SetPixelB(cropped, i - x, j - y, temp_1);
        }
    }
    SaveImage(fname, cropped);
    DeleteImage(image);
    image = NULL;
    return cropped;
}

/* Resize */
Image *Resize(Image *image, int newWidth, int newHeight){

    const char *fname = "smallresize";
    
    unsigned int width = ImageWidth(image);
    unsigned int height = ImageHeight(image);

    float scale_X = (float)newWidth / width;
    float scale_Y = (float)newHeight / height;

    Image *output = CreateImage(newWidth, newHeight);
    
    for (int j = 0; j < newHeight; j++)
    {
        for (int i = 0; i < newWidth; i++)
        {
            int x_og = (float)(i/scale_X);
            int y_og = (float)(j/scale_Y);

            unsigned char temp_1 = GetPixelR(image, x_og, y_og);
            SetPixelR(output, i, j, temp_1);

            temp_1 = GetPixelG(image, x_og, y_og);
            SetPixelG(output, i, j, temp_1);
            
            temp_1 = GetPixelB(image, x_og, y_og);
            SetPixelB(output, i, j, temp_1);
        }
    }
    SaveImage(fname, output);
    DeleteImage(image);
    image = NULL;
    return output;
}



/* Watermark */
Image *Watermark(Image *image, const Image *watermark_image) {
    const char *fname = "watermark";

    unsigned int width = ImageWidth(image);
    unsigned int height = ImageHeight(image);
    unsigned int wm_w = ImageWidth(watermark_image);
    unsigned int wm_h = ImageHeight(watermark_image);

    Image *output = CreateImage(width, height);
    
    for (unsigned int j = 0; j < height; j++){
        for (unsigned int i = 0; i < width; i ++){
            unsigned char r, g, b;
            unsigned char r_n, g_n, b_n;
            
            r_n = GetPixelR(image, i, j);
            g_n = GetPixelG(image, i, j);
            b_n = GetPixelB(image, i, j);

            unsigned int wm_i = i % wm_w;
            unsigned int wm_j = j % wm_h;      
        
            r = GetPixelR(watermark_image, wm_i, wm_j);
            g = GetPixelG(watermark_image, wm_i, wm_j);
            b = GetPixelB(watermark_image, wm_i, wm_j);

            if (r == 0 && g == 0 && b == 0) {
                r_n = 1.45 * r_n;
                if (r_n > 255) r_n = 255;
                g_n = 1.45 * g_n;
                if (g_n > 255) g_n = 255;
                b_n = 1.45 * b_n;
                if (b_n > 255) b_n = 255;
            }
            SetPixelR(output, i, j, r_n);
            SetPixelG(output, i, j, g_n);
            SetPixelB(output, i, j, b_n);
        }
    }
    SaveImage(fname, output);
    DeleteImage(image);
    image = NULL;
    return output;
}


/* Rotate by 90 */
Image *RotateBy90(Image *image, int rotateDirection){

    const char *fname = "rotateby90";
    unsigned int width = ImageWidth(image);
    unsigned int height = ImageHeight(image);
    Image *output = CreateImage(height,width);

    for (unsigned int j = 0; j < height; j++){
        for (unsigned int i = 0; i < width; i++){
            
            unsigned char r, g, b;
            r = GetPixelR(image, i, j);
            g = GetPixelG(image, i, j);
            b = GetPixelB(image, i, j);

            if (rotateDirection == 1){ 
                
                unsigned int y_ccw = width - 1 - i;
                unsigned int x_ccw = j;
         
                SetPixelR(output, x_ccw, y_ccw, r);
                SetPixelG(output, x_ccw, y_ccw, g);
                SetPixelB(output, x_ccw, y_ccw, b);
          
            } else if (rotateDirection == 0){
                
                unsigned int y_cw = i;
                unsigned int x_cw = height - 1 - j;
                
                SetPixelR(output, x_cw, y_cw, r);
                SetPixelG(output, x_cw, y_cw, g);
                SetPixelB(output, x_cw, y_cw, b);
            }
        }
    }
    SaveImage(fname, output);
    DeleteImage(image);
    image = NULL;
    return output;
}
