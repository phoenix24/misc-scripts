(
echo "From: me@xyz.com "
echo "To: them@xyz.com "
echo "MIME-Version: 1.0"
echo "Content-Type: multipart/alternative; " 
echo ' boundary="PAA08673.1018277622/server.xyz.com"' 
echo "Subject: Test HTML e-mail." 
echo "" 
echo "This is a MIME-encapsulated message" 
echo "" 
echo "--PAA08673.1018277622/server.xyz.com" 
echo "Content-Type: text/html" 
echo "" 
echo "<html> 
<head>
<title>HTML E-mail</title>
</head>
<body>
<a href='http://www.google.com'>Click Here</a>
</body>
</html>"
echo "--PAA08673.1018277622/server.xyz.com"
) | sendmail -t
