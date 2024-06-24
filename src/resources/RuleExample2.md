1
 Page 1                                    Saved On:                By
 HFXX_RU_BATCHUPD(RULE);
 +---------------------------------------------------------------------------+
 | Summary : Call this rule to invoke update mode in batch                   |
 | Keywords: FRAMEWORK,BATCH,UPDATE                                          |
 | Unit    : FRAME                                         Library: SITE     |
 +---------------------------------------------------------------------------+
 ------------------------------------------------------------+--------------
 GET HFXX_WT_001;                                            | 1
 HFXX_WT_001.LOCKFAIL_RETRY = 0;                             | 2
 REPLACE HFXX_WT_001;                                        | 3
 CALL HFXX_RU_BATCHUP0(RULE);                                | 4
 ---------------------------------------------------------------------------
 ON GETFAIL :
    HFXX_WT_001.USERID = USERID;
    HFXX_WT_001.LOCKFAIL_RETRY = 0;
    INSERT HFXX_WT_001;
    CALL HFXX_RU_BATCHUP0(RULE);