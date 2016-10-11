$(document).ready(function(){
	// found at http://stackoverflow.com/questions/454202/creating-a-textarea-with-auto-resize
	$('textarea').each(function () {
	  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
	}).on('input', function () {
	  this.style.height = 'auto';
	  this.style.height = (this.scrollHeight) + 'px';
	});
})