var postType;
var postId;
//open report popup
function openForm(type,id) {
  
  postType = type;
  postId = id;
  document.getElementById("reportForm").style.display = "block";
  
}
// close report popup
function closeForm() {
  document.getElementById("reportForm").style.display = "none";
}
//send report details to view.py
function addReport() {
  
  var message =  $('#report-message').val();
  console.log(message);
  if(message == "" || message == " "){
  //if message is empty display error message
  div = document.getElementById("form-container");
  strong = document.createElement("strong");
  strong.innerHTML="Cannot submit report without a message";
  strong.style.color = "red";
  div.appendChild(strong)
  console.log("in report");
  }
  //  call report url in django
  else{
  //send details to views.py
   $.ajax({
    url: '/breakingbread/report/' + postType+'/'+postId+'/',
    data: {
        'message' : message,
        
    },
    dataType: 'json',
    // if database updated successfully refresh the page
    success: function (data) {
        if(data.success) {
          location.reload();
        }

      }
});
}
}