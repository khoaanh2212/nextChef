
function follows_do_follow(chef_id){
    if(user_is_authenticated) {
        var chef = $('#id_chef_' + chef_id);
        var follow_button = chef.find('.follow');
        var follows = chef.find('.follows');
        var counter = follows.find('p');
        var number = parseInt(counter.text());

        if (!follow_button.hasClass('following')) {
            send_follow(chef_id, 1)
            counter.text(number + 1);
            follow_button.addClass('following');
        } else {
            send_follow(chef_id, 0)
            counter.text(number - 1);
            follow_button.removeClass('following');
        }
    }
}

function send_follow(chef_id, following){

    var form_data = {
        "chef_id" : chef_id,
        "following" : following
    }

    $.ajax({
        beforeSend : function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        type : 'POST',
        url : DO_FOLLOW_URL,
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