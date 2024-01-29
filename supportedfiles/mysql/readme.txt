SELECT 
    orderNumber, status, orderDate, requiredDate, comments
FROM
    orders
WHERE
    status = 'Cancelled' 
INTO OUTFILE 'exp_experimentdata.csv' 
FIELDS ENCLOSED BY '"' 
TERMINATED BY ';' 
ESCAPED BY '"' 
LINES TERMINATED BY '\r\n';



'SELECT foo FROM bar' > /tmp/myfile.txt



-----------------

mysql -u root -p < datatocsv.sql