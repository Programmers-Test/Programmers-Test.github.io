<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang ="fr" lang="fr" >
    <head>
        <title>Mini-chat</title>
        <meta  http-equiv=" Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
<?php
if (isset($_POST['nickname']) AND isset($_POST['message']))
{
if ($_POST['nickname'] != NULL AND $_POST['message'] != NULL)
{
// Trước hết, đăng nhập vào MySQL
mysql_connect("localhost", "root", "");
mysql_select_db("tên_CSDL");
//Dùng lệnh sau đây để đề phòng kẻ gian dùng mã HTML độc hại
$message = mysql_real_escape_string(htmlspecialchars($_POST['message']));
$nickname = mysql_real_escape_string(htmlspecialchars($_POST['nickname']));
// Lưu nội dung vào CSDL (mình đã tạo một table mới tên là minichat)
mysql_query("INSERT INTO minichat VALUES('', '$nickname', '$message')");
// Đóng CSDL lại
mysql_close();
}
}
?>
<form action="minichat.php" method= "post">
<p>
Nickname : <input type="text" name= "nickname" /><br>
Message : <input type="text" name= "message" /><br>
<input type="submit" value="Send">
</p>
</form>
<?php
//Cho hiển thị 10 nội dung mới nhất
mysql_connect("localhost", "root", "");
mysql_select_db("tên_CSDL");
$source = mysql_query("SELECT * FROM minichat ORDER BY ID DESC LIMIT 0,10");
mysql_close();
while ($data = mysql_fetch_array($source) )
{
?>
<p>
<strong><?php echo $data['nickname']; ?> </strong> : <?php echo $data['message']; ?>
</p>
<?php
}
// Xong
?>
    </body>
</html>