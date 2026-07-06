
(function(){
  var b=document.querySelector('.burger'), m=document.querySelector('.menu');
  if(b&&m)b.addEventListener('click',function(){m.style.display=(getComputedStyle(m).display==='none'?'flex':'none')});
})();
var WA='34686822291';
function waOpen(msg){var t=encodeURIComponent(msg||'Hola BaggageGo, quiero información.');window.open('https://wa.me/'+WA+'?text='+t,'_blank');return false;}
function quote(){
  var g=function(id){var e=document.getElementById(id);return e?e.value:'';};
  waOpen('Hola BaggageGo 🧳\nQuiero precio para una entrega:\n• Recogida: '+(g('f_from')||'—')+'\n• Entrega: '+(g('f_to')||'—')+'\n• Maletas: '+(g('f_bags')||'—')+'\n• Fecha: '+(g('f_date')||'—'));
}
function sendForm(e){e.preventDefault();var g=function(id){var el=document.getElementById(id);return el?el.value:'';};waOpen('Hola BaggageGo, soy '+g('c_name')+' ('+g('c_email')+').\n'+g('c_msg'));}
