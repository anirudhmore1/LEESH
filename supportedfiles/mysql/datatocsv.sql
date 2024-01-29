SELECT 
    *
FROM
    exp_sarweb.app3_experimentdatastorage
 
INTO OUTFILE '/home/tianzi/projects/github/SARWeb/mysql/exp_experimentdata.csv' 
FIELDS ENCLOSED BY '"' 
TERMINATED BY ';' 
ESCAPED BY '"' 
LINES TERMINATED BY '\r\n';

'SELECT * FROM exp_sarweb.app3_experimentdatastorage' > 'myfile.csv'

mysql -h my.db.com -u usrname--password=pass db_name -e 'SELECT foo FROM bar' > /tmp/myfile.txt