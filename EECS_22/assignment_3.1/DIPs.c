#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "DIPs.h"
#include "FileIO.h"

/* change a color image to black & white */
void BlackNWhite(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
         unsigned char B[WIDTH][HEIGHT])
{
    unsigned char bnw = 0;
    char bwfname[SLEN] = "bw";

    for (int i = 0; i < WIDTH; i++)
    {
        for (int j = 0; j < HEIGHT; j++)
        {
            /* intensity at every pixel */
            bnw = (R[i][j] + G[i][j] + B[i][j]) / 3;

            R[i][j] = bnw;
            G[i][j] = bnw;
            B[i][j] = bnw;
        }
    }
    SaveImage(bwfname, R, G, B);
}

/* reverse image color */
void Negative(unsigned char R[WIDTH][HEIGHT],
          unsigned char G[WIDTH][HEIGHT],
          unsigned char B[WIDTH][HEIGHT])
{
    char negfname[SLEN] = "negative";

    for (int i = 0; i < WIDTH; i++)
    {
        for (int j = 0; j < HEIGHT; j++)
        {
            R[i][j] = 255 - R[i][j];
            G[i][j] = 255 - G[i][j];
            B[i][j] = 255 - B[i][j];
        }
    }
    SaveImage(negfname, R, G, B);
}

/* color filter */
void ColorFilter(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
                 unsigned char B[WIDTH][HEIGHT],
         int target_r, int target_g, int target_b, int threshold,
         int replace_r, int replace_g, int replace_b)
{
    char filterfname[SLEN] = "colorfilter";
    int R_target_min = 0;
    int G_target_min = 0;
    int B_target_min = 0;
    int R_target_max = 0;
    int G_target_max = 0;
    int B_target_max = 0;

    for (int i = 0; i < WIDTH; i++)
    {
        for (int j = 0; j < HEIGHT; j++)
        {
            R_target_min = target_r - threshold;
            R_target_max = target_r + threshold;

            G_target_min = target_g - threshold;
            G_target_max = target_g + threshold;

            B_target_min = target_b - threshold;
            B_target_max = target_b + threshold;

            if (R_target_min >= 0 && R_target_max <= 255
                    && G_target_min >= 0 && G_target_max <= 255
                    && B_target_min >= 0 && B_target_max <= 255)
            {
                if (R[i][j] >= R_target_min && R[i][j] <= R_target_max
                        && G[i][j] >= G_target_min && G[i][j] <= G_target_max
                        && B[i][j] >= B_target_min && B[i][j] <= B_target_max)
                {
                    R[i][j] = replace_r;
                    G[i][j] = replace_g;
                    B[i][j] = replace_b;
                }
                else
                {
                    R[i][j] = R[i][j];
                    G[i][j] = G[i][j];
                    B[i][j] = B[i][j];
                }
            }
        }
    }
    SaveImage(filterfname, R, G, B);
}

/* edge detection */
void Edge(unsigned char R[WIDTH][HEIGHT],
      unsigned char G[WIDTH][HEIGHT],
          unsigned char B[WIDTH][HEIGHT])
{
    char edgefname[SLEN] = "edge";
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
    unsigned char R_new[WIDTH][HEIGHT];
    unsigned char G_new[WIDTH][HEIGHT];
    unsigned char B_new[WIDTH][HEIGHT];

    for (int i = 1; i < WIDTH - 1; i++)
    {
        for (int j = 1; j < HEIGHT - 1; j++)
        {
            I = R[i + 1][j + 1];
            H = R[i + 1][j];
            G_int = R[i + 1][j - 1];
            F = R[i][j + 1];
            E = R[i][j];
            D = R[i][j - 1];
            C = R[i - 1][j + 1];
            B_int = R[i - 1][j];
            A = R[i - 1][j - 1];

            temp_r = (-A - B_int -C - D + 8 * E - F - G_int - H - I);

            if (temp_r < 0) temp_r = 0;
            if (temp_r > 255) temp_r = 255;

            R_new[i][j] = (unsigned char)temp_r;

            I = G[i + 1][j + 1];
            H = G[i + 1][j];
            G_int = G[i + 1][j - 1];
            F = G[i][j + 1];
            E = G[i][j];
            D = G[i][j - 1];
            C = G[i - 1][j + 1];
            B_int = G[i - 1][j];
            A = G[i - 1][j - 1];

            temp_g = (- A - B_int - C - D + 8 * E - F - G_int - H - I);

            if (temp_g < 0) temp_g = 0;
            if (temp_g > 255) temp_g = 255;

            G_new[i][j] = (unsigned char)temp_g;


            I = B[i + 1][j + 1];
            H = B[i + 1][j];
            G_int = B[i + 1][j - 1];
            F = B[i][j + 1];
            E = B[i][j];
            D = B[i][j - 1];
            C = B[i - 1][j + 1];
            B_int = B[i - 1][j];
            A = B[i - 1][j - 1];

            temp_b = (- A - B_int - C - D + 8 * E - F - G_int - H - I);

            if (temp_b < 0) temp_b = 0;
            if (temp_b > 255) temp_b = 255;

            B_new[i][j] = (unsigned char)temp_b;
        }
    }
    SaveImage(edgefname, R_new, G_new, B_new);
}

/* mirror image horizontally */
void HMirror(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
             unsigned char B[WIDTH][HEIGHT])
{
    char hmirfname[SLEN] = "hmirror";

    for (int i = 0; i < WIDTH / 2; i++)
    {
        int r_side = WIDTH - i - 1;
        for (int j = 0; j < HEIGHT; j++)
        {
            unsigned char temp = R[i][j];
            R[i][j] = R[i][j];
            R[r_side][j] = temp;

            temp = G[i][j];
            G[i][j] = G[i][j];
            G[r_side][j] = temp;

            temp = B[i][j];
            B[i][j] = B[i][j];
            B[r_side][j] = temp;

        }
    }
    SaveImage(hmirfname, R, G, B);
}


/* shuffle the image */
void Shuffle(unsigned char R[WIDTH][HEIGHT],
         unsigned char G[WIDTH][HEIGHT],
             unsigned char B[WIDTH][HEIGHT])
{
    char shufffname[SLEN] = "shuffle";
    int block_width = 0;
    int block_height = 0;
    int total = 0;
    unsigned char R_shuf[WIDTH][HEIGHT];
    unsigned char G_shuf[WIDTH][HEIGHT];
    unsigned char B_shuf[WIDTH][HEIGHT];

    block_width = WIDTH/4;
    block_height = HEIGHT/4;
    total = 16;

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

                R_shuf[shuf_c_pos][shuf_r_pos] = R[og_c_pos][og_r_pos];
                G_shuf[shuf_c_pos][shuf_r_pos] = G[og_c_pos][og_r_pos];
                B_shuf[shuf_c_pos][shuf_r_pos] = B[og_c_pos][og_r_pos];
            }
        }
    }
    SaveImage(shufffname, R_shuf, G_shuf, B_shuf);
}

/* pixelate image */
void Pixelate(unsigned char R[WIDTH][HEIGHT],
           unsigned char G[WIDTH][HEIGHT],
               unsigned char B[WIDTH][HEIGHT],
               int block_size)
{
    char pixlfname[SLEN] = "pixelate";
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

    block_r_w = WIDTH % block_size;
    new_w = WIDTH - block_r_w;
    n_blocks_w = new_w / block_size;

    block_r_h = HEIGHT % block_size;
    new_h = HEIGHT - block_r_h;
    n_blocks_h = new_h / block_size;

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
                    r_sum += R[start_x + x][start_y + y];
                    g_sum += G[start_x + x][start_y + y];
                    b_sum += B[start_x + x][start_y + y];
                }
            }

            r_avg = r_sum / (block_size * block_size);
            g_avg = g_sum / (block_size * block_size);
            b_avg = b_sum / (block_size * block_size);

            for (int x = 0; x < block_size; x++)
            {
                for (int y = 0; y < block_size; y++)
                {
                     R[x + start_x][y + start_y] = r_avg;
                     G[x + start_x][y + start_y] = g_avg;
                     B[x + start_x][y + start_y] = b_avg;
                }
            }
        }
    }
    SaveImage(pixlfname, R, G, B);

}

/* flip image vertically */
void VFlip(unsigned char R[WIDTH][HEIGHT],
       unsigned char G[WIDTH][HEIGHT],
           unsigned char B[WIDTH][HEIGHT])
{
    char vflipfname[SLEN] = "vflip";

    for (int j = 0; j < HEIGHT / 2; j++)
    {
        int opp_j = HEIGHT - 1 - j;

        for (int i =0; i < WIDTH; i++)
        {
            unsigned char temp = R[i][j];
            R[i][j] = R[i][opp_j];
            R[i][opp_j] = temp;

            temp = G[i][j];
            G[i][j] = G[i][opp_j];
            G[i][opp_j] = temp;

            temp = B[i][j];
            B[i][j] = B[i][opp_j];
            B[i][opp_j] = temp;

        }
    }
    SaveImage(vflipfname, R, G, B);
}
/**************************************************************/

/* EOF */
