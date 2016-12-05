$( document ).ready(function() {
    console.log( "ready!" );
    $('.addlink.generar').on('click', function(event){return false;});
    console.log($('.addlink.generar'));
  $('.addlink.generar').on('click', function(event){
    console.log("preciono");
    alert($(this).attr('href'));
    /*var ini = $('#id_drf__inicio__gte').val();
    var fin = $('#id_drf__inicio__lte').val();
    if(ini.length > 0 && fin.length > 0){
      var r1 = ini.split("/")
      var r2 = fin.split("/")
      var f1 = new Date(parseInt(r1[1]), parseInt(r1[0])-1 , parseInt(r1[2]));
      var f2 = new Date(parseInt(r2[1]), parseInt(r2[0])-1 , parseInt(r2[2]));
      console.log(f2 >f1);
      if(f2 >f1){*/
      alert("http://127.0.0.1:8001/reporte/get/reporte/?id="+$(this).attr('href'));
      window.location.href = "/reporte/get/reporte/?id="+$(this).attr('href');
      /*}else{
        alert("La fecha de Fin de periodo debe ser mayor, a la de inicio.")
      }
    }else{
      alert("Debe seleccionar el rango de fechas");
    }*/
    //window.open("http://127.0.0.1:8001/reporte/get/reporte/meses/?id="+$(this).attr('href'), '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes')
    return false;
  });
  $('.object-tools:first').prepend("<li><a href=\"#\" class=\"addlink repor_dia\">Reporte del dia</a></li>");
  $('.repor_dia').on('click', function(event){
    window.location.href = "http://127.0.0.1:8001/reporte/get/reporte/dia/";
  });
});
