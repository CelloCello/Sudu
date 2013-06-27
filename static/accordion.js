//var headers = $('#accordion .accordion-header');
var contentAreas = $('#accordion .ui-accordion-content ').hide();
var expandLink = $('.accordion-expand-all');

function accordion_refresh(){
	contentAreas = $('#accordion .ui-accordion-content ').hide();
	contentAreas.unbind('show');
	contentAreas.unbind('hide');
	contentAreas.on({
	    // whenever we open a panel, check to see if they're all open
	    // if all open, swap the button to collapser
	    show: function(){
	        var isAllOpen = !contentAreas.is(':hidden');   
	        if(isAllOpen){
	            expandLink.text('Collapse All')
	                .data('isAllOpen', true);
	        }
	    },
	    // whenever we close a panel, check to see if they're all open
	    // if not all open, swap the button to expander
	    hide: function(){
	        var isAllOpen = !contentAreas.is(':hidden');
	        if(!isAllOpen){
	            expandLink.text('Expand all')
	            .data('isAllOpen', false);
	        } 
	    }
	});
}

$(function(){
	//headers.click(function() {
	//    var panel = $(this).next();
	//    var isOpen = panel.is(':visible');

	//    // open or close as necessary
	//    panel[isOpen? 'slideUp': 'slideDown']()
	//        // trigger the correct custom event
	//        .trigger(isOpen? 'hide': 'show');

	//    // stop the link from causing a pagescroll
	//    return false;
	//});
	//alert(contentAreas);
	expandLink.click(function(){
	    var isAllOpen = $(this).data('isAllOpen');

	    contentAreas[isAllOpen? 'hide': 'show']()
	        .trigger(isAllOpen? 'hide': 'show');
	});

	contentAreas.on({
	    // whenever we open a panel, check to see if they're all open
	    // if all open, swap the button to collapser
	    show: function(){
	        var isAllOpen = !contentAreas.is(':hidden');   
	        if(isAllOpen){
	            expandLink.text('Collapse All')
	                .data('isAllOpen', true);
	        }
	    },
	    // whenever we close a panel, check to see if they're all open
	    // if not all open, swap the button to expander
	    hide: function(){
	        var isAllOpen = !contentAreas.is(':hidden');
	        if(!isAllOpen){
	            expandLink.text('Expand all')
	            .data('isAllOpen', false);
	        } 
	    }
	});	
});
