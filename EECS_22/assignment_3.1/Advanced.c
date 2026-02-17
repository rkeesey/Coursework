#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "DIPs.h"
#include "FileIO.h"
#include "Advanced.h"
#include "Constants.h"
#include <math.h>

/* Create a fisheye image W24 */
void FishEye(unsigned char R[WIDTH][HEIGHT], unsigned char G[WIDTH][HEIGHT], unsigned char B[WIDTH][HEIGHT], double distortion_factor, double k, double scaling_factor)
{
    char fename[SLEN] = "fisheye";

    /*output arrays*/
    unsigned char R_out[WIDTH][HEIGHT];
    unsigned char G_out[WIDTH][HEIGHT]; 
    unsigned char B_out[WIDTH][HEIGHT];

    /*image center*/
    double cent_x = WIDTH/2;
    double cent_y = HEIGHT/2;

    for (int i=0; i<WIDTH; i++)
    {
        for (int j=0; j<HEIGHT; j++)
        {
            /*normalized distance from center*/
            double dx = (i - cent_x)/cent_x;
            double dy = (j - cent_y)/cent_y;
            double radius = sqrt((dx * dx) + (dy * dy));

            /*distortion based off of radius*/
            double distortion = (1.0 + k*radius*radius);

            /*polar coordinate fisheye transformation*/
            double theta = atan2(dy, dx);
            double new_radius = (radius * distortion_factor) / (distortion * scaling_factor);

            /*convert to cartesian coordinates*/
            int x_src = cent_x + (new_radius * cos(theta) * cent_x);
            int y_src = cent_y + (new_radius * sin(theta) * cent_y);

            /*check source coordinate bounds and copy pixel*/
            if (x_src >= 0 && x_src < WIDTH)
            {
                if (y_src >= 0 && y_src < HEIGHT)
                {
                    R_out[i][j] = R[x_src][y_src];
                    G_out[i][j] = G[x_src][y_src];
                    B_out[i][j] = B[x_src][y_src];
                }
                else
                {
                    R_out[i][j] = 0;
                    G_out[i][j] = 0;
                    B_out[i][j] = 0;
                }
            }
        }
    }
    /*copy result back to original image arrays*/
    for (int i=0; i<WIDTH; i++)
    {
        for (int j=0; j<HEIGHT; j++)
        {
            R[i][j] = R_out[i][j];
            G[i][j] = G_out[i][j];
            B[i][j] = B_out[i][j];
        } 
    }
    SaveImage(fename, R, G, B);
}

/* posterize the image */
void Posterize(unsigned char R[WIDTH][HEIGHT], unsigned char G[WIDTH][HEIGHT], unsigned char B[WIDTH][HEIGHT], unsigned int rbits, unsigned int gbits, unsigned int bbits)
{
    char postname[SLEN] = "posterize";

    /*output arrays*/
    unsigned char R_out[WIDTH][HEIGHT];
    unsigned char G_out[WIDTH][HEIGHT]; 
    unsigned char B_out[WIDTH][HEIGHT];

    for (int i=0; i<WIDTH; i++)
    {
        for (int j=0; j<HEIGHT; j++)
        {

            /*mask for specified bit, sets nth bit to 0 andd least n-1 bits to 1*/
            unsigned char r_mask = ~((1U << rbits) - 1);
            unsigned char g_mask = ~((1U << gbits) - 1);
            unsigned char b_mask = ~((1U << bbits) - 1);
            
            /*apply mask to bits*/
            R_out[i][j] = (R[i][j] & r_mask) | ((1U << (rbits - 1)) - 1); 
            G_out[i][j] = (G[i][j] & g_mask) | ((1U << (gbits - 1)) - 1);  
            B_out[i][j] = (B[i][j] & b_mask) | ((1U << (bbits - 1)) - 1);
        
        }
    }
    /*copy result back to original image arrays*/
    for (int i=0; i<WIDTH; i++)
    {
        for (int j=0; j<HEIGHT; j++)
        {
            R[i][j] = R_out[i][j];
            G[i][j] = G_out[i][j];
            B[i][j] = B_out[i][j];
        } 
    }
    SaveImage(postname, R, G, B);
}

/* rotate and zoom the image */
void Rotate(unsigned char R[WIDTH][HEIGHT], unsigned char G[WIDTH][HEIGHT], unsigned char B[WIDTH][HEIGHT], double Angle, double ScaleFactor,  int CenterX, int CenterY)
{

    char rotatename[SLEN] = "rotate";

    /*output arrays*/
    unsigned char R_out[WIDTH][HEIGHT];
    unsigned char G_out[WIDTH][HEIGHT]; 
    unsigned char B_out[WIDTH][HEIGHT];
    
    /*stores memory of original picture size*/
    memset(R_out, 0, sizeof(R_out));
    memset(G_out, 0, sizeof(G_out));
    memset(B_out, 0, sizeof(B_out));

    /*angles*/
    double rad = Angle * PI / 180.000;
    double cosAngle = cos(rad) / ScaleFactor;
    double sinAngle = sin(rad) / ScaleFactor;

    for (int x_dst=0; x_dst<WIDTH; x_dst++)
    {
        for (int y_dst=0; y_dst<HEIGHT; y_dst++)
        {
            /*pixel distance from center of rotation*/
            int trans_x = x_dst - CenterX;
            int trans_y = y_dst - CenterY; 

            /*apply rotation matrix*/
            int i = (int)(cosAngle * trans_x + sinAngle * trans_y + CenterX);
            int j = (int)(-sinAngle * trans_x + cosAngle * trans_y + CenterY);

            /*check source coordinate bounds and copy pixel*/
            if (i >= 0 && i < WIDTH && j >=0 && j < HEIGHT)
            {
                R_out[x_dst][y_dst] = R[i][j];
                G_out[x_dst][y_dst] = G[i][j];
                B_out[x_dst][y_dst] = B[i][j];
            }
            else
            {
                /*pixel value is black if not in range of new rotation bounds*/
                R_out[x_dst][y_dst] = 0;
                G_out[x_dst][y_dst] = 0;
                B_out[x_dst][y_dst] = 0;
            }
        }
    }
    /*copy result back to original image arrays*/
    for (int i=0; i<WIDTH; i++)
    {
        for (int j=0; j<HEIGHT; j++)
        {
            R[i][j] = R_out[i][j];
            G[i][j] = G_out[i][j];
            B[i][j] = B_out[i][j];
        } 
    }
    SaveImage(rotatename, R, G, B);
}

/* motion blur */
void MotionBlur(int BlurAmount, unsigned char R[WIDTH][HEIGHT], unsigned char G[WIDTH][HEIGHT], unsigned char B[WIDTH][HEIGHT])
{
    char blurname[SLEN] = "blur";

    /*output arrays*/
    unsigned char R_out[WIDTH][HEIGHT];
    unsigned char G_out[WIDTH][HEIGHT]; 
    unsigned char B_out[WIDTH][HEIGHT];
    
    for (int i=0; i<WIDTH; i++)
    {
        for (int j=0; j<HEIGHT; j++)
        {
            int sum_R = R[i][j];
            int sum_G = G[i][j];
            int sum_B = B[i][j];

            int count = 1; /*accounts for current pixel value*/

            /*sum pixel values to the right for blur amount range*/
            for (int x=1; x <= BlurAmount; x++)
            {
                if ((x + i) < WIDTH)
                {
                    sum_R += R[x+i][j];
                    sum_G += G[x+i][j];
                    sum_B += B[x+i][j];

                    count++;
                }
            }

            /* averaged pixels to the right */
            int halved_avg_R = sum_R / (2 * count);
            int halved_avg_G = sum_G / (2 * count);
            int halved_avg_B = sum_B / (2 * count);

            int halved_R = R[i][j] / 2;
            int halved_G = G[i][j] / 2;
            int halved_B = B[i][j] / 2;

            /*sum of half of the original value and half of the average*/
            R_out[i][j] = halved_R + halved_avg_R;
            G_out[i][j] = halved_G + halved_avg_G;
            B_out[i][j] = halved_B + halved_avg_B;
        }    
    }

    /*copy result back to original image arrays*/
    for (int i=0; i<WIDTH; i++)
    {
        for (int j=0; j<HEIGHT; j++)
        {
            R[i][j] = R_out[i][j];
            G[i][j] = G_out[i][j];
            B[i][j] = B_out[i][j];
        } 
    }
    SaveImage(blurname, R, G, B);
}
