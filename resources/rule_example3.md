1
 Page 1                                    Saved On:                By
 EMPLOYEES_RAISE(JOBTITLE, REGION);
 LOCAL RAISE, RATE;
 +---------------------------------------------------------------------------+
 | Summary : Call this rule to invoke salary update in batch                 |
 | Keywords: FRAMEWORK,BATCH,UPDATE                                          |
 | Unit    : FRAME                                         Library: SITE     |
 +---------------------------------------------------------------------------+
 JOBTITLE = 'SENIOR ANALYST';                                | Y N N            
 JOBTITLE = 'ANALYST';                                       |   Y N          
 ------------------------------------------------------------+--------------
 RATE = 0.1;                                                 | 1                           
 RATE = 0.05;                                                |   1  
 RATE = 0.02;                                                |     1
 GET EMPLOYEES(REGION) WHERE POSITION = JOBTITLE;            |     2
 FORALL EMPLOYEES.SALARY * RATE;                             | 2 2 3
      EMPLOYEES.SALARY = EMPLOYEES.SALARY + RAISE;           |     
      CALL REPLACE_SALARY(REGION);                           |   
      CALL MSGLOG(EMPLOYEES.LNAME ||‘NOW EARNS‘||            |  
      EMPLOYEES.SALARY);                                     |       
 END;                                                        | 
 ------------------------------------------------------------+--------------
 ON GETFAIL:
   CALL MSGLOG('POSITION IS INVALID');
 ++++++++++++++++++++++++++++
1
 Page 2                                    Saved On:                By
 REPLACE_SALARY(REGION);
 +---------------------------------------------------------------------------+
 | Summary : Call this to replace the salary for a region                    |
 | Keywords:                                                                 |
 | Unit    : SAL                                           Library: SITE     |
 +---------------------------------------------------------------------------+
 ------------------------------------------------------------+--------------
 GET SALARY WHERE REG = REGION;                              | 1
 CALL IS_EQUAL(SALARY.COMP,SALARY.UPD_COMP);                 | 2
 ---------------------------------------------------------------------------
 ON GETFAIL :
    CALL MSGLOG('Missing REGION');
 ++++++++++++++++++++++++++++
1
 Page 3                                    Saved On:                By
 IS_EQUAL(VALUE_A, VALUE_B);
 +---------------------------------------------------------------------------+
 | Summary : check if value A is equal to value B                            |
 | Keywords:                                                                 |
 | Unit    : SAL                                           Library: SITE     |
 +---------------------------------------------------------------------------+
 VALUE_A = VALUE_B;                                          | Y N
 ------------------------------------------------------------+--------------
 SIGNAL EQUAL;                                               | 1
 ---------------------------------------------------------------------------