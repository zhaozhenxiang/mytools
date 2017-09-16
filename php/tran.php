<?php function google_api($ziduan,$a="en"){

if ($a!="en") {

    $zdzhiqian='zh-CN';$zdzhihou='en';

} else {

    $zdzhiqian='en';$zdzhihou='zh-CN';

}

$ziduan=rawurlencode($ziduan);

$ziduan=str_replace("%0D","",$ziduan);

$ziduan=str_replace("%21","!",$ziduan);

$ziduan=str_replace("%2A","*",$ziduan);

$ziduan=str_replace("%28","(",$ziduan);

$ziduan=str_replace("%29",")",$ziduan);

return $jieguo=file("http://translate.google.cn/translate_a/single?client=t&sl=".$zdzhiqian."&tl=".$zdzhihou."&hl=zh-CN&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&pc=1&otf=1&ssel=0&tsel=0&tk=519896|573498&q=".$ziduan)[0].';';

}


var_dump(google_api('我'));