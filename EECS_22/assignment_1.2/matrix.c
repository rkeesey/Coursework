// matrix.c: multiply two 2x2 matrices //
//
// author: Ruby Keesey //
//
// modifications:
// 01/12/2025 RK initial version //

# include <stdio.h>

// input check //
int check_input(const char *prompt, const char *assignment, void *user_input)
{
    // variable definitions and initializations //
    char check;
    int pass;

    // function section //
    do
    {
        printf("%s", prompt); // prints the variable to be assigned //
        pass = scanf(assignment, user_input); // interprets user input //
        if (pass != 1) //checks if user input is valid for assignment type //
        {
            while ((check = getchar()) != '\n'); // clears and reprompts variable until valid user input //
            printf("ERROR: Invalid input.  Please enter numbers only!\n");
        }
    } 
    while (pass != 1);
    while ((check = getchar()) != '\n'); //clears trailing characters after accepted input ('\n')
    // exit //
    return 0;
}

// main function //
int main(void)
{
    // variable definitions and initializations //
    int a11 = 0; // matrix a first column, first row //
    int a12 = 0; // matrix a second column, first row //
    int a21 = 0; // matrix a first column, second row //
    int a22 = 0; // matrix a second column, second row //
    
    int b11 = 0; // matrix b first column, first row //
    int b12 = 0; // matrix b second column, first row //
    int b21 = 0; // matrix b first column, second row //
    int b22 = 0; // matrix b second column, second row //
 
    int p11; // product matrix first column, first row //
    int p12; // product matrix second column, first row //
    int p21; // product matrix first column, second row //
    int p22; // product matrix second column, second row //

    // input section //
    printf("Enter the first matrix(a) that will be multiplied: \n");
    check_input("a11 = ", "%d", &a11);
    check_input("a12 = ", "%d", &a12);
    check_input("a21 = ", "%d", &a21);
    check_input("a22 = ", "%d", &a22);
    
    printf("\nEnter the second matrix(b) that will be multiplied: \n");
    check_input("b11 = ", "%d", &b11);
    check_input("b12 = ", "%d", &b12);
    check_input("b21 = ", "%d", &b21);
    check_input("b22 = ", "%d", &b22);

    // computation section //
    p11 = a11 * b11 + a12 * b21; // product matrix first column, first row // 
    p12 = a11 * b12 + a12 * b22; // product matrix second column, first row //
    p21 = a21 * b11 + a22 * b21; // product matrix first column, second row //
    p22 = a21 * b12 + a22 * b22; // product matrix second column, second row //

    // output section //
    printf("\nResult:\n%d %d\n%d %d\n", p11, p12, p21, p22);

    // exit //
    return 0;
}
// end of main //

//EOF//
