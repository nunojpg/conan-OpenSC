#include <stdio.h>
#include <libopensc/opensc.h>

int main()
{
    printf("OpenSC v%s\n", sc_get_version());
    return 0;
}