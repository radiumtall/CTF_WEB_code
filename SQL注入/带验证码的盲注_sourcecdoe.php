<?php
//a "part" of the source code here

function sqlWaf($s)
{
    $filter = '/xml|extractvalue|regexp|copy|read|file|select|between|from|where|create|grand|dir|insert|link|substr|mid|server|drop|=|>|<|;|"|\^|\||\ |\'/i';
    if (preg_match($filter,$s))
        return False;
    return True;
}

if (isset($_POST['username']) && isset($_POST['password'])) {
    
    if (!isset($_SESSION['VerifyCode']))
            die("?");

    $username = strval($_POST['username']);
    $password = strval($_POST['password']);

    if ( !sqlWaf($password) )
        alertMes('damn hacker' ,"./index.php");

    $sql = "SELECT * FROM users WHERE username='${username}' AND password= '${password}'";
//    password format: /[A-Za-z0-9]/
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if ( $row['username'] === 'admin' && $row['password'] )
        {
            if ($row['password'] == $password)
            {
                $message = $FLAG;
            } else {
                $message = "username or password wrong, are you admin?";
            }
        } else {
            $message = "wrong user";
        }
    } else {
        $message = "user not exist or wrong password";
    }
}

?>