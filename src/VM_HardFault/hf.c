//this is mandatory
#include "zerynth.h"

C_NATIVE(_hf_function){
        C_NATIVE_UNWARN();

        int *armageddon = NULL;
        
        //Don't do it at home!
        *armageddon=0xDEADBEEF;
        
        return ERR_OK; //<-- execution ok, ahaa
}



