#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "Constants.h"
#include "DIPs.h"
#include "FileIO.h"
#include "Advanced.h"
#include "Image.h"
#include "Test.h"

//--------------Function Declarations--------------//
/*menu function*/
void PrintMenu();

//------------Function Defintions-------------//
/*print menu function defintion*/
void PrintMenu() {
    printf("\n----------------------------\n");
    printf("1: Load a PPM image\n");
    printf("2: Save an image in PPM and JPEG format\n");
    printf("3: Change a color image to Black & White\n");
    printf("4: Make a negative of an image\n");
    printf("5: Color filter an image\n");
    printf("6: Sketch the edge of an image\n");
    printf("7: Shuffle an image\n");
    printf("8: Flip an image vertically\n");
    printf("9: Mirror an image horizontally\n");
    printf("10: Add border to an image\n");
    printf("11: Pixelate an image\n");
    printf("12: Shift an image\n");
    printf("13: Crop an image\n");
    printf("14: Resize an image\n");
    printf("15: Add Watermark to an image\n");
    printf("16: Rotate an image by 90 degree\n");
    printf("17: Test all functions\n");
    printf("18: Exit\n");
}

/*main function, calls all DIPs functions*/
int main() {
    
    #ifdef DEBUG
    AutoTest(); /*if debug mode is on, only autotest runs*///
    return 0; /*exit program after photolabtest is performed*/
    
    #else /*run program as usual if debug is off*/
	int option;			/* user input option */
	char fname[SLEN];		/* input file name */
    const char watermarkImgName[SLEN] = "watermark_template";
    Image *watermark_Image = LoadImage(watermarkImgName);
    
    PrintMenu();
	printf("Please make your choice: ");
	scanf("%d", &option);

	int r24 = -1;			/* return code of LoadImage() */
    Image *image = NULL;

	/* ColorFilter() parameters */
	int target_r, target_g, target_b, threshold;
	double factor_r, factor_g, factor_b;
	/* Pixelate() parameter */
	int block_size;

    /* new inputs */
    double base_factor, k, scaling_k_factor, rot_ang, z_scale, x_rot, y_rot;
    unsigned int R_pos, G_pos, B_pos;
    int blur;

    int x, y, W, H;
    int new_x, new_y;
    int rotateDirection; 
    char color[SLEN];
    int border_width;
    int shiftX, shiftY;

	while (option != 18) {
		if (option == 1) {
			printf("Please input the file name to load: ");
			scanf("%75s", fname);
			image = LoadImage(fname);
            if (image == NULL){
                printf("No image to process!\n");
                r24 = -1;
            } else {
                r24 = SUCCESS;
                printf("Image successfully loaded!\n");
            }
		}
		/* menu item 2 - 14 requires image is loaded first */
		else if (option >= 2 && option <= 16) {
			if (r24 != SUCCESS)	 {
				printf("No image to process!\n");
                DeleteImage(image);
                image = NULL;
			}
			/* now image is loaded */
			else {
				switch(option) {
					case 2:
						printf("Please input the file name to save: ");
						scanf("%75s", fname);
						SaveImage(fname, image);
						break;
					case 3:
						BlackNWhite(image);
						printf("\"Black & White\" operation is done!\n");
						break;
					case 4:
						Negative(image);
						printf("\"Negative\" operation is done!\n");
						break;
					case 5:
						printf("Enter Red   component for the target color: ");
						scanf("%d", &target_r);
						printf("Enter Green component for the target color: ");
						scanf("%d", &target_g);
						printf("Enter Blue  component for the target color: ");
						scanf("%d", &target_b);
						printf("Enter threshold for the color difference: ");
						scanf("%d", &threshold);
						printf("Enter value for Red component in the target color: ");
						scanf("%lf", &factor_r);
						printf("Enter value for Green component in the target color: ");
						scanf("%lf", &factor_g);
						printf("Enter value for Blue  component in the target color: ");
						scanf("%lf", &factor_b);
						ColorFilter(image, target_r, target_g, target_b, threshold, factor_r, factor_g, factor_b);
						printf("\"Color Filter\" operation is done!\n");
						break;
					case 6:
						Edge(image);
						printf("\"Edge\" operation is done!\n");
						break;
					case 7:
						Shuffle(image);
						printf("\"Shuffle\" operation is done!\n");
						break;
					case 8:
						VFlip(image);
						printf("\"VFlip\" operation is done!\n");
						break;
					case 9:
						HMirror(image);
						printf("\"HMirror\" operation is done!\n");
						break;
                    case 10:
						printf("Enter border width: ");
						scanf("%d", &border_width);
                        printf("Available border colors: black, white, red, green, blue, yellow, cyan, pink, orange\n");
						printf("Select border color from the options: ");
						scanf("%s", color);
                        AddBorder(image, color, border_width);
						printf("\"Border\" operation is done!\n");
                        break;
					case 11:
						printf("Enter pixelate block size: ");
						scanf("%d", &block_size);
						Pixelate(image, block_size);
						printf("\"Pixelate\" operation is done!\n");
						break;
                    case 12:
						printf("Enter the shift width: ");
						scanf("%d", &shiftX);
						printf("Enter the shift height: ");
						scanf("%d", &shiftY);
                        Shift(image, shiftX, shiftY);
                        break;
                    case 13: 
                        printf("Please enter the X offset value: ");
                        scanf("%d", &x);
                        printf("Please enter the Y offset value: ");
                        scanf("%d", &y);
                        printf("Please enter the crop width: ");
                        scanf("%d", &W);
                        printf("Please enter the crop height: ");
                        scanf("%d", &H);
                        
                        Crop(image, x, y, W, H);
                        printf("\"Crop\" operation is done!");
                        break;
                    case 14:
                        printf("Please enter the new image width: ");
                        scanf("%d", &new_x);
                        printf("Please enter the new image height: ");
                        scanf("%d", &new_y);
                        
                        Resize(image, new_x, new_y);
                        printf("\"Resizing the image\" operation is done!");
                        break;
                    case 15: 
                        image = Watermark(image, watermark_Image);
                        break;
                    case 16:
                        
                        printf("Please input the direction of rotation (0:clockwise, 1:counterclockwise): ");
                        scanf("%d", &rotateDirection);
                        image = RotateBy90(image, rotateDirection);
                        break;
                    default:
                        break;

				}
			}
		}
		else if (option == 17) {
            AutoTest();
            if (AutoTest() != 0) {
                printf("AutoTest failed, error code RC.");
            }
            printf("Autotest finished successfully.");
			r24 = SUCCESS;	/* set returned code SUCCESS, since image is loaded */
        }else {
			printf("Invalid selection!\n");
		}

		/* Process finished, waiting for another input */
		PrintMenu();
		printf("Please make your choice: ");
		scanf("%d", &option);
	}
	printf("You exit the program.\n");
	return 0;
    #endif
}

//EOF//
