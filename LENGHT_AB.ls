!RESULT PR
:R[150]=AR[1];

!REAL POINT 1
:R[151]=AR[2];

!REAL POINT 2
:R[152]=AR[3];

:PR[R[150]]=PR[R[152]]-PR[R[151]];
:PR[R[150]]=PR[R[150]]*PR[R[150]];
:PR[R[150]]=PR[1,R[150]]+PR[2,R[150]]+PR[3,R[150]];
:PR[R[150]]=SQRT(PR[R[150]]);

9.9487

