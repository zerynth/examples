//this is mandatory
#include "zerynth.h"

//declare "normal" C function
int32_t gimme_zero();


// define C/Python interface function:
//_my_c_function must be defined with the C_NATIVE macro
// must return an error code to signal the result of the execution
// and must set the value of *res to the return value of the corresponding
// Python function (c_division in main.py)
C_NATIVE(_my_c_function){
        C_NATIVE_UNWARN();

        //parse the Python arguments
        //if they are not integers, raise TypeError
        int32_t a,b,c;
    	if (parse_py_args("ii",nargs,args,&a,&b)!=2)
    		return ERR_TYPE_EXC;   //<-- this is the macro

        if (b==gimme_zero())
            return ERR_ZERODIV_EXC; //<-- oops, raise ZeroDivisionError

    	*res = PSMALLINT_NEW(a/b);  //<-- return the integer division to Python

        return ERR_OK; //<-- execution ok
}


//"normal" C functions can also be defined!
int32_t gimme_zero(){
    return 0;
}