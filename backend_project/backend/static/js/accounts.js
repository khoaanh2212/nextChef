
$(document).ready(function(){
	if( $('#login_form').length > 0 ){
		var form = $('#login_form');
		var button = form.find('#facebook_login');
		button.click(function(evt){
			evt.preventDefault();
			facebookLogIn();
		});
	}
	
	if( $('#signup_form').length > 0 ){
		var form = $('#signup_form');
		var button = form.find('#facebook_register');
		button.click(function(evt){
			evt.preventDefault();
			facebookSignUp();
		});
	}
});

function facebookSignUp() {
	facebookCheckStatus(facebookSignUpCallback);
}

function facebookLogIn() {
	facebookCheckStatus(facebookLogInCallback);
}

function facebookConnect() {
	facebookCheckStatus(facebookConnectCallback);
}

function facebookCheckStatus(callback) {
	FB.getLoginStatus(function(response) {
		// Check if is logged in FB
		if (response.status != 'connected') {
			FB.login(function(response) {
				callback(response);
			}, {
				scope : 'email'
			});
		} else {
			callback(response);
		}
	});
}

function facebookConnectCallback(logInResponse){
	facebookSendForm(logInResponse, FACEBOOK_CONNECT_URL);
}

function facebookSignUpCallback(logInResponse) {
	facebookSendForm(logInResponse, FACEBOOK_SIGNUP_URL);
}
	
function facebookLogInCallback(logInResponse) {	
	facebookSendForm(logInResponse, FACEBOOK_LOGIN_URL);
}

function facebookSendForm(logInResponse, action) {
	var csrftoken = getCookie('csrftoken');
	if (logInResponse.authResponse) {
		FB.api('/me', function(meResponse) {
			var last_name;
			if (meResponse.middle_name)
				last_name = meResponse.middle_name + ' ' + meResponse.last_name;
			else
				last_name = meResponse.last_name;
			var male = (meResponse.gender == "male") ? 1 : 0;
			var form = $('<form>');
			form.attr({
				method : 'post',
				action : action,
			}).append($('<input>').attr({
				type : 'hidden',
				name : 'csrfmiddlewaretoken',
				value : csrftoken,
			})).append($('<input>').attr({
				type : 'text',
				name : 'first_name',
				value : meResponse.first_name
			})).append($('<input>').attr({
				type : 'text',
				name : 'last_name',
				value : last_name
			})).append($('<input>').attr({
				type : 'text',
				name : 'email',
				value : meResponse.email
			})).append($('<input>').attr({
				type : 'text',
				name : 'picture',
				value : 'https://graph.facebook.com/' + meResponse.id + '/picture'
			})).append($('<input>').attr({
				type : 'text',
				name : 'user_id',
				value : logInResponse.authResponse.userID
			})).append($('<input>').attr({
				type : 'text',
				name : 'token',
				value : logInResponse.authResponse.accessToken
			})).append($('<input>').attr({
				type : 'text',
				name : 'male',
				value : male
			}));
			
			var type = $('#id_type');
			if(type.length>0){
				form.append(type);
			}else{
               // If the user try to loggin and he is not in the
               // system we will registered him like a foodie.
               form.append($('<input>').attr({
				    type : 'text',
				    name : 'type',
				    value : 0
               }));
            }
			
			form.submit();
			
		});
	}
}
