EMPLOYEES_RAISE(JOBTITLE, REGION);
_ LOCAL RAISE, RATE;
_ ------------------------------------------------------------------------
_ JOBTITLE = 'SENIOR ANALYST'; ¦ Y N N            
_ JOBTITLE = 'ANALYST'; ¦   Y N          
_ ------------------------------------------------------------------------
_ RATE = 0.1; ¦ 1                           
_ RATE = 0.05; ¦   1  
_ RATE = 0.02; ¦     1
_ GET EMPLOYEES(REGION) WHERE POSITION = JOBTITLE; ¦     2
_ FORALL EMPLOYEES.SALARY * RATE;                  ¦ 2 2 3
_      EMPLOYEES.SALARY = EMPLOYEES.SALARY + RAISE;¦     
_      CALL REPLACE_SALARY(REGION);                ¦   
_      CALL MSGLOG(EMPLOYEES.LNAME ||‘NOW EARNS‘|| ¦  
_      EMPLOYEES.SALARY);                          ¦       
_ END; ¦ 
_ -------------------------------------------------------------------------
ON GETFAIL:
CALL ENDMSG('POSITION IS INVALID'); 
