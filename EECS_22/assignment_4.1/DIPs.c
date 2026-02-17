#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "DIPs.h"
#include "FileIO.h"

/* Shift an image */
Image *Shift(Image *image, int shiftX, int shiftY){

    const char *fname = "shift";

    unsigned int width = ImageWidth(image);
    unsigned int height = ImageHeight(image);
    
    Image *shift = CreateImage(width, height);
   
    for (int i=0; i<width; i++) { 
        for (int j=0; j<height; j++){ 

            int x = (i + shiftX + width) % width; 
            int y = (j + shiftY + height) % height;

            int r = GetPixelR(image, i, j);
            int g = GetPixelG(image, i, j);
            int b = GetPixelB(image, i, j);
            
            SetPixelR(shift, x, y, r);
            SetPixelG(shift, x, y, g);
            SetPixelB(shift, x, y, b);
        }
    }

    SaveImage(fname, shift);
    DeleteImage(image);
    image = NULL;
    return shift;
}

Image *AddBorder(Image *image, char *color, int border_width) {
    const char *fname = "border";

    unsigned int width = ImageWidth(image);
    unsigned int height = ImageHeight(image);

    // Create output image
    Image *ab_img = CreateImage(width, height);

    // Initialize color to white (default)
    unsigned int r = 255, g = 255, b = 255;

    // Set border color based on input
    if (strcmp(color, "black") == 0) {
        r = 0, g = 0, b = 0;
    } else if (strcmp(color, "white") == 0) {
        r = 255, g = 255, b = 255;
    } else if (strcmp(color, "red") == 0) {
        r = 255, g = 0, b = 0;
    } else if (strcmp(color, "green") == 0) {
        r = 0, g = 255, b = 0;
    } else if (strcmp(color, "blue") == 0) {
        r = 0, g = 0, b = 255;
    } else if (strcmp(color, "yellow") == 0) {
        r = 255, g = 255, b = 0;
    } else if (strcmp(color, "cyan") == 0) {
        r = 0, g = 255, b = 255;
    } else if (strcmp(color, "pink") == 0) {
        r = 255, g = 192, b = 203;
    } else if (strcmp(color, "orange") == 0) {
        r = 255, g = 165, b = 0;
    } else {
        fprintf(stderr, "Error: Unknown color.\n");
        return NULL;
    }

    // Add border //
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            if (i < border_width || j < border_width ||
                i >= width - border_width || j >= height - border_width) {
                // Border color //
                SetPixelR(ab_img, i, j, r);
                SetPixelG(ab_img, i, j, g);
                SetPixelB(ab_img, i, j, b);
            } else {
                // copy original image inside border//
                SetPixelR(ab_img, i, j, GetPixelR(image, i, j));
                SetPixelG(ab_img, i, j, GetPixelG(image, i, j));
                SetPixelB(ab_img, i, j, GetPixelB(image, i, j));
            }
        }
    }

    SaveImage(fname, ab_img);
    DeleteImage(image);
    image = NULL;
    return ab_img;
}

/* change a color image to black & white */
Image *BlackNWhite(Image *image){
    
    unsigned char bnw = 0;
    const char *bwfname = "bw";

    Image *bwimg = CreateImage(image->W, image->H);

    for (int i = 0; i < image->W; i++)
    {
        for (int j = 0; j < image->H; j++)
        {
            /* intensity at every pixel */
            unsigned char tmp_R = GetPixelR(image, i, j);
            unsigned char tmp_G = GetPixelG(image, i, j);
            unsigned char tmp_B = GetPixelB(image, i, j);

            bnw = (tmp_R + tmp_G + tmp_B) / 3;

            SetPixelR(bwimg, i, j, bnw);
            SetPixelG(bwimg, i, j, bnw);
            SetPixelB(bwimg, i, j, bnw);
        }
    }
    SaveImage(bwfname, bwimg);
    DeleteImage(image);
    image = NULL;
    return bwimg;
}

/* reverse image color */
Image *Negative(Image *image){

    const char *negfname = "negative";

    Image *neg_img = CreateImage(image->W, image->H);

    for (int i = 0; i < image->W; i++)
    {
        for (int j = 0; j < image->H; j++)
        {

            /* intensity at every pixel */
            unsigned char tmp_R = GetPixelR(image, i, j);
            unsigned char tmp_G = GetPixelG(image, i, j);
            unsigned char tmp_B = GetPixelB(image, i, j);

            tmp_R = 255 - tmp_R;
            tmp_G = 255 - tmp_G;
            tmp_B = 255 - tmp_B;

            SetPixelR(neg_img, i, j, tmp_R);
            SetPixelG(neg_img, i, j, tmp_G);
            SetPixelB(neg_img, i, j, tmp_B);          
        }
    }
    SaveImage(negfname, neg_img);
    DeleteImage(image);
    image = NULL;
    return neg_img;
}

/* color filter */
Image *ColorFilter(Image *image,
         int target_r, int target_g, int target_b, int threshold,
         int replace_r, int replace_g, int replace_b)
{
    char *filterfname = "colorfilter";
    int R_target_min = 0;
    int G_target_min = 0;
    int B_target_min = 0;
    int R_target_max = 0;
    int G_target_max = 0;
    int B_target_max = 0;

    Image *filter_img = CreateImage(image->W, image->H);

    for (int i = 0; i < image->W; i++)
    {
        for (int j = 0; j < image->H; j++)
        {
            R_target_min = target_r - threshold;
            R_target_max = target_r + threshold;

            G_target_min = target_g - threshold;
            G_target_max = target_g + threshold;

            B_target_min = target_b - threshold;
            B_target_max = target_b + threshold;

            /* intensity at every pixel */
            unsigned char tmp_R = GetPixelR(image, i, j);
            unsigned char tmp_G = GetPixelG(image, i, j);
            unsigned char tmp_B = GetPixelB(image, i, j);

            if (R_target_min >= 0 && R_target_max <= 255
                    && G_target_min >= 0 && G_target_max <= 255
                    && B_target_min >= 0 && B_target_max <= 255)
            {
                if (tmp_R >= R_target_min && tmp_R <= R_target_max
                        && tmp_G >= G_target_min && tmp_G <= G_target_max
                        && tmp_B >= B_target_min && tmp_B <= B_target_max)
                {
                    SetPixelR(filter_img, i, j, replace_r);
                    SetPixelG(filter_img, i, j, replace_g);
                    SetPixelB(filter_img, i, j, replace_b);          
                }
                else
                {
                    SetPixelR(filter_img, i, j, tmp_R);
                    SetPixelG(filter_img, i, j, tmp_G);
                    SetPixelB(filter_img, i, j, tmp_B);          
                }
            }
        }
    }
    SaveImage(filterfname, filter_img);
    DeleteImage(image);
    image = NULL;
    return filter_img;
}

/* edge detection */
Image *Edge(Image *image){

    const char *edgefname = "edge";
    int A = 0;
    int B_int = 0;
    int C = 0;
    int D = 0;
    int E = 0;
    int F = 0;
    int G_int = 0;
    int H = 0;
    int I = 0;
    int temp_r;
    int temp_g;
    int temp_b;

    Image *edg_img = CreateImage(image->W, image->H);

    for (int i = 1; i < image->W - 1; i++)
    {
        for (int j = 1; j < image->H - 1; j++)
        {

            int next_x = i + 1;
            int past_x = i - 1;

            int next_y = j + 1;
            int past_y = j - 1;

            I = GetPixelR(image, next_x, next_y);
            H = GetPixelR(image, next_x, j);
            G_int = GetPixelR(image, next_x, past_y);
            F = GetPixelR(image, i, next_y);
            E = GetPixelR(image, i, j);
            D = GetPixelR(image, i, past_y);
            C = GetPixelR(image, past_x, next_y);
            B_int = GetPixelR(image, past_x, j);
            A = GetPixelR(image, past_x, past_y);

            temp_r = (-A - B_int -C - D + 8 * E - F - G_int - H - I);

            if (temp_r < 0) temp_r = 0;
            if (temp_r > 255) temp_r = 255;

            SetPixelR(edg_img, i, j, temp_r);

            I = GetPixelG(image, next_x, next_y);
            H = GetPixelG(image, next_x, j);
            G_int = GetPixelG(image, next_x, past_y);
            F = GetPixelG(image, i, next_y);
            E = GetPixelG(image, i, j);
            D = GetPixelG(image, i, past_y);
            C = GetPixelG(image, past_x, next_y);
            B_int = GetPixelG(image, past_x, j);
            A = GetPixelG(image, past_x, past_y);

            temp_g = (-A - B_int -C - D + 8 * E - F - G_int - H - I);

            if (temp_g < 0) temp_g = 0;
            if (temp_g > 255) temp_g = 255;

            SetPixelG(edg_img, i, j, temp_g);

            I = GetPixelB(image, next_x, next_y);
            H = GetPixelB(image, next_x, j);
            G_int = GetPixelB(image, next_x, past_y);
            F = GetPixelB(image, i, next_y);
            E = GetPixelB(image, i, j);
            D = GetPixelB(image, i, past_y);
            C = GetPixelB(image, past_x, next_y);
            B_int = GetPixelB(image, past_x, j);
            A = GetPixelB(image, past_x, past_y);

            temp_b = (-A - B_int -C - D + 8 * E - F - G_int - H - I);

            if (temp_b < 0) temp_b = 0;
            if (temp_b > 255) temp_b = 255;

            SetPixelB(edg_img, i, j, temp_b);
        }
    }
    SaveImage(edgefname, edg_img);
    DeleteImage(image);
    image = NULL;
    return edg_img;
}

/* mirror image horizontally */
Image *HMirror(Image *image){
    const char *hmirfname = "hmirror";

    Image *hmir_img = CreateImage(ImageWidth(image), ImageHeight(image));
    
    for (int i = 0; i < image->W/2; i++)
    {
        for (int j = 0; j < image->H; j++)
        {
            unsigned char temp = GetPixelR(image, i, j);
            SetPixelR(hmir_img, i, j, temp);

            temp = GetPixelG(image, i, j);
            SetPixelG(hmir_img, i, j, temp);
            
            temp = GetPixelB(image, i, j);
            SetPixelB(hmir_img, i, j, temp);
        }
    }

    for (int i = image->W/2; i < image->W; i++)
    {
        int l_side = image->W - i - 1;
        for (int j = 0; j < image->H; j++)
        {
            unsigned char temp = GetPixelR(image, l_side, j);
            SetPixelR(hmir_img, i, j, temp);

            temp = GetPixelG(image, l_side, j);
            SetPixelG(hmir_img, i, j, temp);
            
            temp = GetPixelB(image, l_side, j);
            SetPixelB(hmir_img, i, j, temp);
        }
    }
    SaveImage(hmirfname, hmir_img);
    DeleteImage(image);
    image = NULL;
    return hmir_img;
}

/* Shuffle operation */
Image *Shuffle(Image *image)
{
    const char *shufffname = "shuffle";
    int block_width = 0;
    int block_height = 0;
    int total = 0;

    unsigned int width = ImageWidth(image);
    unsigned int height = ImageHeight(image);

    block_width = width/4;
    block_height = height/4;
    total = 16;

    Image *shuf_img = CreateImage(ImageWidth(image), ImageHeight(image));
    
    for (int block = 0; block < total; block++)
    {
        int target = 15 - block;

        int row_og = (block / 4) * block_height;
        int col_og = (block % 4) * block_width;
        int row_shuff = (target / 4) * block_height;
        int col_shuff = (target % 4) * block_width;

        for (int i = 0; i < block_height; i++)
        {
            for (int j = 0; j < block_width; j++)
            {
                int og_r_pos = row_og + i;
                int og_c_pos = col_og + j;
                int shuf_r_pos = row_shuff + i;
                int shuf_c_pos = col_shuff + j;

                unsigned int r, g, b; 

                r = GetPixelR(image, og_c_pos, og_r_pos);
                g = GetPixelG(image, og_c_pos, og_r_pos);
                b = GetPixelB(image, og_c_pos, og_r_pos);

                SetPixelR(shuf_img, shuf_c_pos, shuf_r_pos, r);
                SetPixelG(shuf_img, shuf_c_pos, shuf_r_pos, g);
                SetPixelB(shuf_img, shuf_c_pos, shuf_r_pos, b);
            }
        }
    }
    SaveImage(shufffname, shuf_img);
    DeleteImage(image);
    image = NULL;
    return shuf_img;
}

/* pixelate image */
Image *Pixelate(Image *image, int block_size){

    const char *pixlfname = "pixelate";
    int block_r_w = 0;
    int new_w = 0;
    int n_blocks_w = 0;
    int block_r_h = 0;
    int new_h = 0;
    int n_blocks_h = 0;
    int start_y = 0;
    int start_x = 0;
    int r_sum = 0;
    int g_sum = 0;
    int b_sum = 0;
    int r_avg = 0;
    int g_avg = 0;
    int b_avg = 0;

    block_r_w = image->W % block_size;
    new_w = image->W - block_r_w;
    n_blocks_w = new_w / block_size;

    block_r_h = image->H % block_size;
    new_h = image->H - block_r_h;
    n_blocks_h = new_h / block_size;

    Image *pixl = CreateImage(image->W, image->H);
    
    for (int i=0; i < n_blocks_w; i++)
    {
        for (int j=0; j < n_blocks_h; j++)
        {
            start_x = i * block_size;
            start_y = j * block_size;

            r_sum = 0;
            g_sum = 0;
            b_sum = 0;

            for (int x = 0; x < block_size; x++)
            {
                for (int y = 0; y < block_size; y++)
                {
                    int x_idx = start_x + x;
                    int y_idx = start_y + y;

                    r_sum += GetPixelR(image, x_idx, y_idx);
                    g_sum += GetPixelG(image, x_idx, y_idx);
                    b_sum += GetPixelB(image, x_idx, y_idx);
                }
            }

            r_avg = r_sum / (block_size * block_size);
            g_avg = g_sum / (block_size * block_size);
            b_avg = b_sum / (block_size * block_size);

            for (int x = 0; x < block_size; x++)
            {
                for (int y = 0; y < block_size; y++)
                {
                     int x_idx = start_x + x;
                     int y_idx = start_y + y;

                     SetPixelR(pixl, x_idx, y_idx, r_avg);
                     SetPixelG(pixl, x_idx, y_idx, g_avg);
                     SetPixelB(pixl, x_idx, y_idx, b_avg);
                }
            }
        }
    }
    SaveImage(pixlfname, pixl);
    DeleteImage(image);
    image = NULL;
    return pixl;
}

/* flip image vertically */
Image *VFlip(Image *image){
    const char *vflipfname = "vflip";

    Image *vflip = CreateImage(image->W, image->H);

    for (int j = 0; j < image->H / 2; j++)
    {
        int opp_j = image->H - 1 - j;

        for (int i =0; i < image->W; i++)
        {
            unsigned char temp_1 = GetPixelR(image, i, j);
            unsigned char temp_2 = GetPixelR(image, i, opp_j);
            SetPixelR(vflip, i, j, temp_2);
            SetPixelR(vflip, i, opp_j, temp_1);

            temp_1 = GetPixelG(image, i, j);
            temp_2 = GetPixelG(image, i, opp_j);
            SetPixelG(vflip, i, j, temp_2);
            SetPixelG(vflip, i, opp_j, temp_1);

            temp_1 = GetPixelB(image, i, j);
            temp_2 = GetPixelB(image, i, opp_j);
            SetPixelB(vflip, i, j, temp_2);
            SetPixelB(vflip, i, opp_j, temp_1);
        }
    }
    SaveImage(vflipfname, vflip);
    DeleteImage(image);
    image = NULL;
    return vflip;
}
/**************************************************************/

/* EOF */
