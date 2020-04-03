// Sidebar Click Event
function SideBarAddClick() {
	$('nav.navbar>div.navbar-header>button').on('click', function () {
		$('#sidebar').toggleClass('active');
	});
}

// 체크박스, 라디오버튼, datepicker 적용
function SetFormDecoFirstInit() {
	IboxInputUISet();
	// datepicker 적용
	$('.input-group.date').datepicker({
		language:'ko',
		format: 'yyyy-mm-dd',
		todayBtn: "linked",
		keyboardNavigation: false,
		forceParse: false,
		calendarWeeks: false,
		autoclose: true,
	});
	//$(".input-group.date").datepicker("setDate", new Date());
}

// 체크박스, 라디오버튼 꾸미기
function IboxInputUISet(obj) {
	if (obj == undefined) {

		$('.i-checks').iCheck({
			checkboxClass: 'icheckbox_square-green',
			radioClass: 'iradio_square-green',
		});
	} else {
		$(obj+' .i-checks').iCheck({
			checkboxClass: 'icheckbox_square-green',
			radioClass: 'iradio_square-green',
		});
	}
}

// Handlebars 의 리스트 형식 체우기
function hbs(sourceId, data, resultId, callback) {
	var source = $("#"+sourceId).html();
	var template = Handlebars.compile(source);
	var html = template(data);
	$("#"+resultId).empty().append(html);
	if (callback instanceof Function) {
		callback();
	}
}

// 메뉴바 강제 닫기
function SideBarClose() {
	var chkval = $("#sidebar").css('margin-left');
	if (chkval == '0px') {
		$('nav.navbar>div.navbar-header>button').click();
	}
}

// 지정 Object로 스크롤 이동
function TargetScrollMove(target) {
	var offset = $(target).offset();
	$('html, body').animate({scrollTop: (offset.top - 20)}, 400);

}

// 스크롤바 보유 유무
$.fn.hasScrollBar = function() {
	return (this.prop("scrollHeight") == 0 && this.prop("clientHeight") == 0)
		|| (this.prop("scrollHeight") > this.prop("clientHeight"));
};

// Draggable 지정(x축)
function ObjectDraggable(target, parent) {
	$('#'+target).draggable({
		axis:"x",
	    scroll: false,
		//grid: [20, 0],
		stop: function( event, ui ) {
			var pw = $("#"+parent).width();
			var pc = $("#"+target).width();
			var x1 = pw - pc;
			//var x2 = pc - pw;
			//console.log(pw, pc, x1, x2, ui.position.left);
			//console.log(typeof x1, typeof ui.position.left);

			// 우측 끝에 만난 경우
			if (ui.position.left <= x1) {
				//console.log("넘는다", ui.position.left);
				$("#"+target).css('left', (x1 - 3)+"px");
			}
			// 좌측 끝에 만난 경우
			if (ui.position.left > 0) {
				//console.log("넘는다", ui.position.left);
				$("#"+target).css('left', "0px");
			}


		}
	});
}

// 스크롤바 없는 Object에 x축 Draggable 지정
function ObjectDraggable_Horizontal(target) {
	var parent = $('#'+target).parent();
	$('#'+target).draggable({
		axis:"x",
	    scroll: false,
		//grid: [20, 0],
		stop: function( event, ui ) {
			var pw = $(parent).width();
			var pc = $("#"+target).width();
			var sc = 0;
			if ($(parent).hasScrollBar()) sc = 19;
			var x1 = pw - pc - sc;
			// 우측 끝에 만난 경우
			if (ui.position.left <= x1) {
				//console.log("넘는다", ui.position.left);
				$("#"+target).css('left', x1+"px");
			}
			// 좌측 끝에 만난 경우
			if (ui.position.left > 0) {
				//console.log("넘는다", ui.position.left);
				$("#"+target).css('left', "0px");
			}


		}
	});
}

// 스크롤바 없는 Object에 y축 Draggable 지정
function ObjectDraggable_Vertical(target) {
	var parent = $('#'+target).parent();
	$('#'+target).draggable({
		axis:"y",
	    scroll: false,
		//grid: [20, 0],
		stop: function( event, ui ) {
			var ph = $(parent).height();
			var phc = $("#"+target).height();
			var y = ph - phc;
			// 바닥 끝에 만난 경우
			if (ui.position.top <= y) {
				//console.log("넘는다", ui.position.left);
				$("#"+target).css('top', (y - 3)+"px");
			}
			// 상단 끝에 만난 경우
			if (ui.position.top > 0) {
				//console.log("넘는다", ui.position.left);
				$("#"+target).css('top', "0px");
			}
		}
	});
}

// 스크롤바 존재하는 Object에 axis 지정에 따라 마우스 드래그로 자동 스크롤(target는 Jquery 셀렉터를 넘김)
function SliderDragAdd(target, axis='xy') {
	const slider = target;
	let isDown = false;
	let startX;
	let startY;
	slider.on('mousedown', (e) => {
	  isDown = true;
	  startX = Math.abs(e.pageX);
	  startY = Math.abs(e.pageY);
	});
	slider.on('mouseleave', () => {
	  isDown = false;
	});
	slider.on('mouseup', () => {
	  isDown = false;
	});
	slider.on('mousemove', (e) => {
		if(!isDown) return;
		e.preventDefault();
		// X축이라면
		if (axis.indexOf('x') !== -1) {
			const x = Math.abs(e.pageX) - startX;
			let walk = slider.scrollLeft() - x * 0.10; //scroll-slow
			const maxRange = slider.prop("scrollWidth") - parseInt(slider.css("width"));
			if (walk > maxRange) walk = maxRange;
			else if (walk < 0) walk = 0;
			slider.scrollLeft(walk);
			
		}
		// Y축이라면
		if (axis.indexOf('y') !== -1) {
			const y = Math.abs(e.pageY) - startY;
			let walk = slider.scrollTop() - y * 0.10; //scroll-slow
			const maxRange = slider.prop("scrollHeight") - parseInt(slider.css("height"));
			if (walk > maxRange) walk = maxRange;
			else if (walk < 0) walk = 0;
			slider.scrollTop(walk);
		}
	});
}

	/*
	// css의 요소나 class를 변경시
	var observer = new MutationObserver(function(mutations) {
		console.log(mutations);
		console.log('size changed!');
		console.log($(".modal-custom").height());
	});
	var target = document.querySelector('.modal-custom');
	observer.observe(target, {
		attributes: true,
		childList: true,
		characterData: true
	});
	*/


// modal-custom (position:fixed 인 div) 수직 중앙 위치 시키기
$.fn.center = function(type) {
	if (type==undefined) type="both";
	if (type=="top" || type=="both") {
		if ($(window).height() <= 768) {
			this.css("top", 0);
		} else {
			this.css("top", Math.max(0, ($(window).height() - $(this).outerHeight()) / 2));
		}
	}
	if (type=="left" || type=="both") {
		if ($(window).height() <= 768) {
			this.css("left", 0);
		} else {
			this.css("left", Math.max(0, ($(window).width() - $(this).outerWidth()) / 2));
		}

	}
	return this;
}

// Table 체크박스 전체 선택/해제 이벤트
function CheckboxAllProc(tableid, callback) {
	$("#"+tableid+" thead .icheckbox_square-green .iCheck-helper").on('click', function() {
		if ($("#"+tableid+" thead .icheckbox_square-green").hasClass('checked')) {
			$("#"+tableid+" tbody INPUT[type=checkbox]").attr('checked', true) ;
			$("#"+tableid+" tbody .icheckbox_square-green").addClass('checked');
		} else {
			$("#"+tableid+" tbody INPUT[type=checkbox]").attr('checked', false);
			$("#"+tableid+" tbody .icheckbox_square-green").removeClass('checked');
		}
		if (typeof callback == "function") callback();
	});
}

// 리스트의 페이징 HTML 반환
function HtmlListPaging(page=1, block_count=10) {
	var html = '<nav>';
		html += '<ul class="pagination pagination-sm">';
		html += '<li>';
		html += '<a href="#" aria-label="Previous">';
		html += '<span aria-hidden="true">&laquo;</span>';
		html += '</a>';
		html += '</li>';
		for(var i=0; i<block_count; i++) {
			if (i + 1 == page) {
				html += '<li class="active"><a href="#">' + page + '</a></li>';
			} else {
				html += '<li><a href="#">' + (i + 1) + '</a></li>';
			}
		}
		html += '<li>';
		html += '<a href="#" aria-label="Next">';
		html += '<span aria-hidden="true">&raquo;</span>';
		html += '</a>';
		html += '</li>';
		html += '</ul>';
		html += '</nav>';

	return html;
}

// Json Array 의 중복 제거 반환 : https://ddalpange.github.io/2017/10/10/js-not-duplicated-object-array/
function getUniqueObjectArray(array, key) {
	var tempArray = [];
	var resultArray = [];
	for(var i = 0; i < array.length; i++) {
		var item = array[i]
		if(tempArray.indexOf(item[key]) !== -1) {
			continue;
		} else {
			resultArray.push(item);
			tempArray.push(item[key]);
		}
	}
	return resultArray;
}

// Json 값으로 일치하는 항목 반환
function getSelectReturnObjectArray(jsonobj, key, value) {
	return jsonobj.filter(function(obj) {
			return obj[key] === value;
		});
}

