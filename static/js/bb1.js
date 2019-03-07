var speed2=80; //数字越大速度越慢
var tab3=document.getElementById("neiye_demo3");
var tab4=document.getElementById("neiye_demo4");
var tab5=document.getElementById("neiye_demo5");
tab5.innerHTML=tab4.innerHTML;
function Marquee(){
if(tab5.offsetWidth-tab3.scrollLeft<=0)
tab3.scrollLeft-=tab4.offsetWidth
else{
tab3.scrollLeft++;
}
}
var MyMar=setInterval(Marquee,speed);
tab.onmouseover=function() {clearInterval(MyMar)};
tab.onmouseout=function() {MyMar=setInterval(Marquee,speed)};