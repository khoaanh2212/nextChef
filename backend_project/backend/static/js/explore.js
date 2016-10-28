$(document).ready(function(){
	
	$('#activation_modal').modal('show');
	
	$('#nux_modal').modal('show');
	
	$('.carousel').carousel({
		interval: 4000
	});
	
	$('.carousel-caption').click(function(){
		document.location.href = $(this).attr('data-url');
	});
	
	/*$('#global_navbar').addClass('landing');*/

	$(window).scroll(function(){
		var underHeader = $(window).scrollTop() > $('.header').outerHeight() - $('#global_navbar').height()
            - $('.accept-cookies').outerHeight();
		/*if(underHeader){
			$('#global_navbar').removeClass('landing');
		}else{
			$('#global_navbar').addClass('landing');
		}*/
		
		if(underHeader){
			$('#explore .navbar').addClass('fixed');
		}else{
			$('#explore .navbar').removeClass('fixed');
		}
		
		var load_more = (window.innerHeight + window.scrollY) >= $(document).height() - 400;
		/*console.log('window.innerHeight: ' + window.innerHeight);
		console.log('window.scrollY: ' + window.scrollY);
		console.log('document.body.offsetHeight: ' + $(document).height());*/
		if(load_more) {
			var scope = angular.element(document.getElementById('explore')).scope();
			scope.loadMore();
			scope.$apply();
	    }
		
	})
});