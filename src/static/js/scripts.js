var sorterExtraction = function(el) {
	var $el = $(el);
	
	var src = $el.attr('data-source');
	
	if (src) {
		return src;
	}
	
    var s = $el.text();
    
    s = s.replace("Č", "CZ");
    s = s.replace("Ć", "CZ");
    s = s.replace("Đ", "DZ");
    s = s.replace("Š", "SZ");
    s = s.replace("Ž", "ZZ");
    s = s.replace("č", "cz");
    s = s.replace("ć", "cz");
    s = s.replace("đ", "dz");
    s = s.replace("š", "sz");
    s = s.replace("ž", "zz");
    
    return s;
};

$(function(){
	$('.sortable').tablesorter({
        textExtraction: sorterExtraction
    });
	
	$('.table-pager').each(function(){
		var $this = $(this);
		var $pager = $this.find('.pager');
		$this.find('table').tablesorterPager({
			container: $pager,
			positionFixed: false
		});
	});
	
	/* c = &#x10D;, s = &#x161; z = &#x17E; C = &#x10C; S = &#x160; Z = &#x17D; */
	$.datepicker.regional['slo'] = {
		closeText: 'Zapri',
		prevText: '&lt;Prej&#x161;nji',
		nextText: 'Naslednji&gt;',
		currentText: 'Trenutni',
		monthNames: ['Januar','Februar','Marec','April','Maj','Junij',
		'Julij','Avgust','September','Oktober','November','December'],
		monthNamesShort: ['Jan','Feb','Mar','Apr','Maj','Jun',
		'Jul','Avg','Sep','Okt','Nov','Dec'],
		dayNames: ['Nedelja','Ponedeljek','Torek','Sreda','&#x10C;etrtek','Petek','Sobota'],
		dayNamesShort: ['Ned','Pon','Tor','Sre','&#x10C;et','Pet','Sob'],
		dayNamesMin: ['Ne','Po','To','Sr','&#x10C;e','Pe','So'],
		weekHeader: 'Teden',
		dateFormat: 'dd.mm.yy',
		firstDay: 1,
		isRTL: false,
		showMonthAfterYear: false,
		yearSuffix: ''
	};
	
	$.datepicker.setDefaults($.datepicker.regional['slo']);
	
	$('.button.delete').click(function(){
		return confirm('Te akcije ni mogoče razveljaviti! Ali ste prepričani?');
	});
});