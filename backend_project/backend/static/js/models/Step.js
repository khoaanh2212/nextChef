app.factory('Step', ['$http', function($http) {
    
    function Step(stepData) {
    	this.cover= false;
    	this.creation_date= "";
		this.drag_thumb= "";
		this.edit_date= "";
		this.edit_thumb= "";
		this.id= 0;
		this.instructions= "";
		this.order= 1;
		this.quantity= 0;
		this.temperature= 0;
		this.time= 0;
	    this.progress_loaded = 0;
		this.progress_total = 100;
		this.recipe_id = -1;
		try {
            this.uploadPhotoUrl= RECIPE_UPLOAD_PHOTO_URL;
        }catch(err) { }
        try {
            this.deletePhotoUrl= STEP_DELETE_PHOTO_URL;
        }catch(err) { }
        try {
            this.updateInstructionsUrl= STEP_UPDATE_INSTRUCTIONS_URL;
        }catch(err) { }
        try {
            this.changePhotoOrderUrl= STEP_CHANGE_PHOTO_ORDER_URL;
        }catch(err) { }
        try {
            this.selectAsCoverUrl= RECIPE_SELECT_COVER_URL;
        }catch(err) { }
        
        if (stepData) {
            this.setData(stepData);
        }
    };
    
    Step.prototype = {
        
        setData: function(stepData) {
            angular.extend(this, stepData);
        },
        uploadPhoto: function(photoFile, controllerScope, callback) {
        	this.uploading = true;
        	this.progress_loaded = 0;
        	this.progress_total = 100;
        	var scope = this;
            var fd = new FormData();
            fd.append('photo', photoFile);
            fd.append('order', this.order)
            
            $.ajax({
    	        url: this.uploadPhotoUrl.replace('RECIPE_ID', this.recipe_id), 
    	        type: 'POST',
    	        // Custom XMLHttpRequest
    	        xhr: function(){  
    	            var myXhr = $.ajaxSettings.xhr();
    	            // Check if upload property exists
    	            if(myXhr.upload){ 
    	            	// For handling the progress of the upload
    	                myXhr.upload.addEventListener('progress', function(e){
    	        		    if(e.lengthComputable){
    	        		    	scope.progress_loaded = e.loaded;
    	        		    	scope.progress_total = e.total;
    	        		    	controllerScope.$apply.apply(controllerScope, []);
    	        		    }
    	                }, false); 
    	            }
    	            return myXhr;
    	        },
    	        beforeSend : function(xhr, settings) {
					if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
						xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
					}
				},
    	        success: function(results){
    	        	if(results.success){
            			scope.setData(results.step_data);
            			scope.uploading = false;
            		}
    	        	callback(scope, results);
    	        },
    	        data: fd,
    	        cache: false,
    	        contentType: false,
    	        processData: false
    	    });
            
            /* PROGRESS STILL NOT SUPPORTED BY ANGULAR
            return $http.post(this.uploadPhotoUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}}).success(function(results) {
        		if(results.success){
        			scope.setData(results.step_data);
        			scope.uploading = false;
        		}
        	});*/
        },
        selectAsCover: function(){
        	this.cover = true;
        	return $http.post(this.selectAsCoverUrl.replace('PHOTO_ID', this.id));
        },
        updateOrder: function(){
        	return $http.post(this.changePhotoOrderUrl.replace('PHOTO_ID', this.id), $.param({'photo_order':this.order}));
        },
        updateInstructions: function(){
        	return $http.post(this.updateInstructionsUrl.replace('PHOTO_ID', this.id), $.param({'instructions':this.instructions}));
        },
        deleteStep: function(){
        	return $http.post(this.deletePhotoUrl.replace('PHOTO_ID', this.id));
        }
    };
    return Step;
}]);