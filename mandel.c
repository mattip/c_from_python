int mandel(float x, float y, int max_iters, unsigned char * val)
{
    int i = 0;
    float cR = x;
    float cI = y;
    float zR = 0;
    float zI = 0;
    for (i = 0; i < max_iters; i++)
    {
        /* in complex notation, z * z + c */
        zR = zR * zR - zI * zI + cR;
        zI = 2 * zR * zI + cI;
        if ((zR * zR + zI * zI) >= 4)
        {
            *val = i;
            return 0;
        }
    }
    *val = max_iters;
    return 1;
}
