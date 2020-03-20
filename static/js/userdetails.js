var fileList = [];
var step = 1;

function openDialog() {
    document.getElementById('fileid').click();
}
function readURL(event) {
    var selectedFile = event.target.files[0];
    var reader = new FileReader();
    var imgtag = document.getElementById("profilepic");
    // console.log(imgtag);
    reader.onload = function(event) {
        imgtag.src = event.target.result;
    };
    reader.readAsDataURL(selectedFile);
}
function showDetails() {
    $('.myDetails').css('display','block');
    $('.uploadNew').css('display','none');
    $('.myreports').css('display','none');
    document.getElementById('formTitle').innerHTML = 'My Details'
}
function uploadNewRecipe() {
    $('.uploadNew').css('display','block');
    $('.myreports').css('display','none');
    $('.myDetails').css('display','none');
    document.getElementById('formTitle').innerHTML = 'Upload Recipe'
}
function showMyReports() {
    $('.myreports').css('display','block');
    $('.uploadNew').css('display','none');
    $('.myDetails').css('display','none');
    document.getElementById('formTitle').innerHTML = 'My Reports'
   
}
function navigateToHomePage() {
    window.history.back();
}
function updateList() {
    var input = document.getElementById('fileElementId');
    output = document.getElementById('fileList');
    var children = "";
    for (var i = 0; i < input.files.length; ++i) {
        fileList.push(input.files[i]);
        // children += '<li>' + input.files.item(i).name + '</li>';
    }
    for(var i = 0; i < fileList.length; i++) {
        console.log(fileList[i]);
        children += '<li>' + fileList[i].name + '</li>';
    }
    console.log(children);
    output.innerHTML = '<ul>' + children + '</ul>'
}
function addAnotherStep() {
    step++;
    var newdiv = document.createElement('div');
    newdiv.innerHTML = "<label> Step " + step + "</label>" ;
    newdiv.innerHTML += " <input class='form-control' type='text' name='steps[]'/>"
    document.getElementById('stepsRecipe').appendChild(newdiv);
}
function saveRecipe() {
    var recipeName =  $('#recipeName').val();
    var cuisine =  $('#cuisine').val();
    var time_taken =  $('#time_taken').val();
    var type =  $('#type').val();
    var level =  $('#level').val();
    var ingredients =  $('#ingredients').val();
    var category =  $('#category').val();
    var steps = $("input[name='steps[]']")
              .map(function(){return $(this).val();}).get();
    console.log(steps);
}
