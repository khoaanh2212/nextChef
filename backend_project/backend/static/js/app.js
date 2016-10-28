
var app = angular.module('cookbooth', ['ui.bootstrap']);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Accept'] = 'application/json, text/javascript, */*; q=0.01';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
}]);

$(document).ready(function(){
	
	$.smartbanner();
	
    if( getCookie('cookies-accepted') == null ){

        var accept_cookies_box = $('<div class="accept-cookies" style="display: none;">');
        var close_button = $('<a class="close gtm-event" href="#" data-gtme-category="Navbar" data-gtme-action="Click" data-gtme-tag="accept_cookies">x</a>');
        close_button.click(function(){
            accept_cookies_box.slideUp(300);
            setCookie('cookies-accepted', true, 365);
            $('#global_navbar').removeClass('cookies');
            $('#check-cookies').css('height', 60);
        });

        accept_cookies_box.append(close_button);
        accept_cookies_box.append($('<p>We use cookies to give you the best online experience. By using our website you agree to our use of cookies in accordance with our <a href="http://blog.nextchef.co/cookies-policy/">Cookie Policy</a>.</p>'));

        $('body').prepend(accept_cookies_box);
        accept_cookies_box.slideDown(300);
        $('#global_navbar').addClass('cookies');
        $('#check-cookies').css('height', 137);
    }

    $('.search-bar input').keypress(function(evt){
        if ( evt.which == 13 ) {
            document.location.href = SEARCH_URL + '?' + $.param({q:$(this).val()});
        }
    });

    $('#search_more_results_button').click(function(evt){
        evt.preventDefault();
        var query = $('.search-bar input').val().replace(' ','+');
        document.location.href = SEARCH_URL + '?q=' + query;
    });

    var execute_search_timer = null;
    var send_search_event_timer = null;
    
    $('.search-bar input').keyup(function(evt){
        if ( evt.which != 13 ) {
            var $this = $(this);

            if(execute_search_timer != null){
                clearTimeout(execute_search_timer);
            }

            execute_search_timer = setTimeout(
                function(){

                    var query = $this.val();
                    var results_list = $('.search-bar .results');

                    if (query != '' && query.length > 2) {
                        var form_data = {
                            'q': query
                        }
                        
                        if(typeof dataLayer != 'undefined' && dataLayer != null){
	                        if(send_search_event_timer != null){
	                            clearTimeout(send_search_event_timer);
	                        }
	                        send_search_event_timer = setTimeout(function(){
	                        	/* Google Tag Manager Event */
	                            dataLayer.push({'event': 'search-event'});
	                        }, 1000);
	                    }
                        
                        var url = results_list.attr('data-search-url');
                        var csrftoken = getCookie('csrftoken');
                        $.ajax({
                            beforeSend: function (xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            },
                            type: 'GET',
                            url: url,
                            dataType: "json",
                            data: form_data,
                            success: function (data) {

                                var recipe = null;
                                if(data.count>0){

                                    results_list.empty();
                                    for (var i = 0; i < data.results.length; i++) {
                                        recipe = data.results[i];

                                        if (recipe.name.length > 36) {
                                            recipe.name = recipe.name.substring(0, 30) + " . . .";
                                        }

                                        var li = "<li>" +
                                            "<a class='gtm-event' href='" + recipe.recipe_url + "' data-gtme-category='Navbar' data-gtme-action='Search Click' data-gtme-tag='result'>" +
                                            "<div class='image' style='background-image:url(" + recipe.image_url + ");'></div>" +
                                            "<div class='data'>" +
                                            "<strong>" + recipe.name + "</strong>" +
                                            "<small>" + recipe.chef_full_name + "</small>" +
                                            "</div>" +
                                            "</a>" +
                                            "</li>";

                                        results_list.append(li);
                                        execute_search_timer = null;
                                    }

                                    $('.search-bar .results-wrapper').slideDown(150);

                                }else{
                                    $('.search-bar .results-wrapper').slideUp(150, function(){
                                        results_list.empty();
                                    });
                                }


                            },
                            error: function (){
                                $('.search-bar .results-wrapper').slideUp(150);
                                execute_search_timer = null;
                            }
                        });
                    } else {
                        $('.search-bar .results-wrapper').slideUp(150, function(){
                            results_list.empty();
                        });
                    }
                },
                300
            );

        }
    });


    $('.search-button').click(function(evt){
        evt.preventDefault();
        var search_bar = $('.search-bar');
        if(search_bar.is(':visible')){
            search_bar.slideUp(150, function(){
                $('.search-bar .results-wrapper').slideUp(150, function(){
                    $('.search-bar .results').empty();
                });
            });
        }else{
            search_bar.find('input').val('');
            search_bar.slideDown(150, function(){
                $('.search-bar input').focus();
            });
            $(".triangle").css('left', $('.search-button').offset().left + 17 );
        }
    });
});

function checkAuthenticated(text){
	if(!AUTHENTICATED){
		scope = angular.element(document.getElementById('body')).scope();
		scope.checkAuthenticated(text)
		scope.$apply();
		return false;
	}
	return true;
}

function setCookie(c_name, value, exdays) {
	var exdate = new Date();
	exdate.setDate(exdate.getDate() + exdays);
	var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
	document.cookie = c_name + "=" + c_value;
}

function setCookieSeconds(name, value, seconds) {
	var date = new Date();
	date.setTime(date.getTime() + (seconds * 1000));
	var expires = "; expires=" + date.toGMTString();
	document.cookie = name + "=" + value + expires + "; path=/";
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for ( var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function deleteCookie(c_name) {
    document.cookie = encodeURIComponent(c_name) + "=deleted; expires=" + new Date(0).toUTCString();
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/')
			|| (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
			// or any other URL that isn't scheme relative or absolute i.e
			// relative.
			!(/^(\/\/|http:|https:).*/.test(url));
}

var slug = function(str) {
	  str = str.replace(/^\s+|\s+$/g, ''); // trim
	  str = str.toLowerCase();

	  // remove accents, swap ñ for n, etc
	  var from = "ãàáäâẽèéëêìíïîõòóöôùúüûñç·/_,:;";
	  var to   = "aaaaaeeeeeiiiiooooouuuunc------";
	  for (var i=0, l=from.length ; i<l ; i++) {
	    str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
	  }

	  str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
	.replace(/\s+/g, '-') // collapse whitespace and replace by -
	.replace(/-+/g, '-'); // collapse dashes

	  return str;
};