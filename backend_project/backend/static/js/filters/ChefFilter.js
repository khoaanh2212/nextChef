app.filter('chefFilter', function() {
	return function(data, chef_id, different) {
		var filtered = [];
	    if (different == 0) {
	    	return data;
	    }else{
	    	for (var i=0;i<data.length;i++) {
	    		var value = data[i];
	    		if (different<0 && value.chef_id == chef_id || different>0 && value.chef_id != chef_id) {
	    			filtered.push(value);
	    		}
	    	}
	    }
	    return filtered;
	  }
	});