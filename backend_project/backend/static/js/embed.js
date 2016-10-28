$(document).ready(function(){
	$('#show_ingredients_button').click(function(){
		$('.ingredients-wrapper ul').toggle(300);
		if($(this).hasClass('active')){
			$(this).removeClass('active');
		}else{
			$(this).addClass('active');
		}
	});
	
	$('.show-instructions-button').click(function(){
		$('.instructions-text').toggle(300);
		if($(this).hasClass('active')){
			$('.show-instructions-button').removeClass('active');
		}else{
			$('.show-instructions-button').addClass('active');
		}
	});
	
	$('.layout, .cover, .carousel-control, .logo').mouseover(function(){
		$('.layout').css('opacity',0.8);
	}).mouseleave(function(){
		$('.layout').css('opacity',0);
	});

    $('#steps-carousel').keyup(function(event) {
        if (event.which == '37') {
            $('.carousel').carousel('prev');
        } else if (event.which == '39') {
            $('.carousel').carousel('next');
        }
    });
});