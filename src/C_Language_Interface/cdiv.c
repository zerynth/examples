//always include zerynth.h
#include "zerynth.h"

//declare "normal" C function
int32_t gimme_zero();


// define C/Python interface function:
//_my_c_function must be defined with the C_NATIVE macro
// must return an error code to signal the result of the execution
// and must calle MAKE_RESULT to the return value of the corresponding
// Python function (c_division in main.py)
C_NATIVE(_my_c_function){
        C_NATIVE_UNWARN();
        int32_t a,b,c;

        
        //first check the arguments type: if they are not integers, raise TypeError
        PYC_CHECK_ARG_INTEGER(0);
        PYC_CHECK_ARG_INTEGER(1);

        //parse the Python arguments: convert from Python to C format
        a = PYC_ARG_INT(0);  //get argument 0 as integer
        b = PYC_ARG_INT(1);  //get argument 1 as integer

        if (b==gimme_zero())
            return ERR_ZERODIV_EXC; //<-- oops, raise ZeroDivisionError

        MAKE_RESULT(PSMALLINT_NEW(a/b)); // <-- return the integer division to Python

        return ERR_OK; //<-- execution ok
}

//"normal" C functions can also be defined!
int32_t gimme_zero(){
    return 0;
}
