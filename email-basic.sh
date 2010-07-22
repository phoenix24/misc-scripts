#!/bin/bash
#requires: date,sendmail
function fappend {
    echo "$2">>$1;
}
YYYYMMDD=`date +%Y%m%d`

# CHANGE THESE
TOEMAIL="recipient@email.com";
FREMAIL="crondaemon@65.101.11.232";
SUBJECT="Daily Backup - $YYYYMMDD";
MSGBODY="This is your daily backup notice";

# DON'T CHANGE ANYTHING BELOW
TMP="/tmp/tmpfil_123"$RANDOM;

rm -rf $TMP;
fappend $TMP "From: $FREMAIL";
fappend $TMP "To: $TOEMAIL";
fappend $TMP "Reply-To: $FREMAIL";
fappend $TMP "Subject: $SUBJECT";
fappend $TMP "";
fappend $TMP "$MSGBODY";
fappend $TMP "";
fappend $TMP "";
cat $TMP|sendmail -t;
rm $TMP;

