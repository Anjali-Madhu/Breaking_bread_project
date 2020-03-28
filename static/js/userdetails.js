var fileList = [];
var step = 1;

$(document).ready(function ()
 {
  $('#cuisine').on('change',function ()
  {
    var cuisine = $(this).val();
    if(cuisine == "Others"){
        document.getElementById("cuisine_input").style.display = "block";
        }
        });
});

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
    $('.myreports').css('display','block');
    $('.uploadNew').css('display','none');
    $('.myDetails').css('display','none');
    
    document.getElementById('formTitle').innerHTML = 'Reports against me'
   
}
function navigateToHomePage() {
    window.history.back();
}
function addPictures() {
    var input = document.getElementById('fileElementId');
    output = document.getElementById('fileList');
    var children = "";
    for (var i = 0; i < input.files.length; ++i) {
        fileList.push(input.files[i]);
        // children += '<li>' + input.files.item(i).name + '</li>';
    }
    for(var i = 0; i < fileList.length; i++) {
        // console.log(fileList[i]);
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
    var responseId;
    var levelType = {'Beginner':0, 'Intermediate':1, 'Expert':2}
    var cookingType = {'Non-Vegetarian':0, 'Vegetarian':1, 'Vegan':2}

    var recipeName =  $('#recipeName').val();
    var cuisine =  $('#cuisine').val();
    if(cuisine=="Others"){
        cuisine = $('#cuisine_type').val()
    }
    var time_taken =  $('#time_taken').val();
    var type = cookingType[$('#type').val()];
    var level = levelType[$('#level').val()];
    var ingredients =  $('#ingredients').val().replace(/,/g, '?').replace(/\n|\r/g, ""); //replace all comma by '?'
    console.log(ingredients);
    var category =  $('#category').val();
    var steps = $("input[name='steps[]']")
            .map(function(){return $(this).val();}).get();

    var msg = "";
    if(fileList.length == 0) {
        msg += 'Please upload at least one photo of the recipe.' + '\n'
        // alert('Please upload at least one photo of the recipe');
    }
    if(recipeName == "") {
        msg += 'Please enter the recipe name.' + '\n'
        // alert('Please enter the recipe name');
    }
    if(ingredients == "") {
        msg += 'Please enter the ingredients for this recipe.' + '\n'
        // alert('Please enter the ingredients for this recipe');
    }
    if(time_taken == "") {
        msg += 'Please enter the time taken for this recipe.' + '\n'
        // alert('Please enter the time taken for this recipe');
    }
    
    if(steps.length <1) {
        msg += 'Please enter the steps for this recipe.' + '\n'+steps.length
    }
    if(msg == "") {
        $("#preloader").css("display", "block");        
        var desc = "";
        if(steps.length > 1) {
            for(let i = 0; i < steps.length; i++) {
                if(i == 0)  
                    desc = steps[i];
                else 
                    desc += "?" + steps[i]
            }
        }
        //call uploadrecipe url in django
        $.ajax({
            url: '/breakingbread/uploadrecipe',

            data: {
                'recipeName' : recipeName,
                'cuisine' : cuisine,
                'time_taken' : time_taken,
                'type' : type,
                'level' : level,
                'ingredients' : ingredients,
                'category' : category,
                'desc' : desc,
            },
            dataType: 'json',
            success: function (data) {
                responseId = data.recipeId;
            }
        });
        // //upload image
        setTimeout(function(){
            if(responseId && responseId != undefined) {
                console.log('responId', responseId);
                var formdata = new FormData();
                formdata.append('number', fileList.length);
                formdata.append('recipeId', responseId);
                for(let i = 0; i < fileList.length; i++) {
                    let title = 'image' + i;
                    formdata.append(title, fileList[i]);
                }
                var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                $.ajax({
                    beforeSend: function(request) {
                        request.setRequestHeader("X-CSRFToken", csrftoken);
                    }, 
                    url: '/breakingbread/uploadrecipe/',
                    type: 'POST',
                    data: formdata,
                    async: true,
                    cache: false,
                    contentType: false,
                    processData: false,
                    data: formdata,
                    dataType: 'json',
                    success: function (data) {
                        if(data.success) {
                            $("#preloader").css("display", "none");
                            swal("Recipe uploaded successfully", "", "success").then((goToRecipe) => {
                                if(goToRecipe) {
                                    window.location.href = '/breakingbread/recipe/' + responseId;
                                }
                            });
                        
                        }
                    }
                });
            }
        }, 3500);
    }
    else {
        alert(msg);
    }
}
