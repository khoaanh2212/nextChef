
function do_love(recipe_id){
	
	checkAuthenticated('love');
	
    if(user_is_authenticated){
        var recipe = $('#id_recipe_' + recipe_id);
        var love = recipe.find('.loves');
        var counter = love.find('p');
        var number = parseInt(counter.text());

        if(!love.hasClass('loved')){
            send_love(recipe_id, 1)
            counter.text(number + 1);
            love.addClass('loved');
        }else{
            send_love(recipe_id, 0)
            counter.text(number - 1);
            love.removeClass('loved');
        }
    }
}

function send_love(recipe_id, loved){

    var form_data = {
        "recipe_id" : recipe_id,
        "loved" : loved
    }

    $.ajax({
        beforeSend : function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        type : 'POST',
        url : DO_LOVE_URL,
        dataType : "json",
        data : form_data,
        success : function(data) {
            console.log(data);
        },
        error : function(data) {
            console.log(data);
        }
    });
}