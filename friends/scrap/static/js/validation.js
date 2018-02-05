
$(document).on("click", "#sub_fb", function(event){

id=$('#fb_id').val();

if (id=='')

  {
    document.getElementById('fb_id').focus();
    return false
  }
$('#loading').css('display','block');

$.ajax({
  url: '/home',
  method: 'POST',
  data: {'id': id,'csrfmiddlewaretoken': token},
  success: function(response){
    // alert(JSON.stringify(response));
    var content = response;
    if(content.length<=0){
      $('#result_data').html("No record found");
    }
    else {
      var table_content = "<center><table border='1'><thead><tr><th>Rank</th><th>Country</th><th>Percentage</th></tr></thead><tbody>";
      var count=0;
      for(i=content.length;i>=0;i--){
        $.each(content[i], function(j, value) {
          if(j != 'unknown'){
              count=count+1;
              table_content += "<tr><td>"+count+"</td><td>"+j+"</td><td>"+Math.round(value * 100) / 100+" %</td></tr>"
          }
        });
      }

      table_content +="</tbody></table></center>";
      $('#result_data').html(table_content);
    }
    $('#loading').css('display','none');
  }

})

});
