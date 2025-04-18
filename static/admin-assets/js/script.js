$(document).ready(function () {
	// Variables declarations
	var $wrapper = $('.main-wrapper,.broker-dashboard-wrapper');
	var $slimScrolls = $('.slimscroll');
	var $pageWrapper = $('.page-wrapper');
	feather.replace();
	// Page Content Height Resize
	$(window).resize(function () {
		if ($('.page-wrapper').length > 0) {
			var height = $(window).height();
			$(".page-wrapper").css("min-height", height);
		}
	});
		// Mobile menu sidebar overlay
		$('body').append('<div class="sidebar-overlay"></div>');
		$(document).on('click', '#mobile_btn', function () {
			$wrapper.toggleClass('slide-nav');
			$('.sidebar-overlay').toggleClass('opened');
			$('body').addClass('mini-sidebar');
			$('html').addClass('menu-opened');
			$('#task_window').removeClass('opened');
			return false;
		});

		$(".sidebar-overlay").on("click", function () {
			$('html').removeClass('menu-opened');
			$(this).removeClass('opened');
			$wrapper.removeClass('slide-nav');
			$('.sidebar-overlay').removeClass('opened');
			$('#task_window').removeClass('opened');
		});

	if ($('.datatable').length > 0) {
		$('.datatable').DataTable({
			"bFilter": false,
			"bPaginate": false,
			"aaSorting": [],
			'aoColumnDefs': [{
				'bSortable': false,
				'aTargets': [-1]
			}],
		});
	}

	// Sidebar Slimscroll
	if ($slimScrolls.length > 0) {
		$slimScrolls.slimScroll({
			height: 'auto',
			width: '100%',
			position: 'right',
			size: '7px',
			color: '#ccc',
			wheelStep: 10,
			touchScrollStep: 100
		});
		var wHeight = $(window).height() - 60;
		$slimScrolls.height(wHeight);
		$('.sidebar .slimScrollDiv').height(wHeight);
		$(window).resize(function () {
			var rHeight = $(window).height() - 60;
			$slimScrolls.height(rHeight);
			$('.sidebar .slimScrollDiv').height(rHeight);
		});
	}

	// Sidebar
	var Sidemenu = function () {
		this.$menuItem = $('#sidebar-menu a');
	};

	function init() {
		var $this = Sidemenu;
		$('#sidebar-menu a').on('click', function (e) {
			if ($(this).parent().hasClass('submenu')) {
				e.preventDefault();
			}
			if (!$(this).hasClass('subdrop')) {
				$('ul', $(this).parents('ul:first')).slideUp(250);
				$('a', $(this).parents('ul:first')).removeClass('subdrop');
				$(this).next('ul').slideDown(350);
				$(this).addClass('subdrop');
			} else if ($(this).hasClass('subdrop')) {
				$(this).removeClass('subdrop');
				$(this).next('ul').slideUp(350);
			}
		});
		$('#sidebar-menu ul li.submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
	}


	init();
	$(document).on('mouseover', function (e) {
		e.stopPropagation();
		if ($('body').hasClass('mini-sidebar') && $('#toggle_btn').is(':visible')) {
			var targ = $(e.target).closest('.sidebar, .header-left').length;
			if (targ) {
				$('body').addClass('expand-menu');
				$('.subdrop + ul').slideDown();
			} else {
				$('body').removeClass('expand-menu');
				$('.subdrop + ul').slideUp();
			}
			return false;
		}
	});

	$(document).on('click', '#toggle_btn', function () {
		if ($('body').hasClass('mini-sidebar')) {
			$('body').removeClass('mini-sidebar');
			$(this).addClass('active');
			$('.subdrop + ul');
			setTimeout(function () {
				$("body").removeClass("mini-sidebar");
				$(".header-left").addClass("active");
			}, 100);
		} else {
			$('body').addClass('mini-sidebar');
			$(this).removeClass('active');
			$('.subdrop + ul');
			setTimeout(function () {
				$("body").addClass("mini-sidebar");
				$(".header-left").removeClass("active");
			}, 100);
		}
		return false;
	});
	$(document).on('click', '.sidebar-backshadow', function () {
		$('body').removeClass('mini-sidebar');
		$('html').removeClass('menu-opened');
	});
	
	// toggle-password
	if ($('.toggle-password').length > 0) {
		$(document).on('click', '.toggle-password', function () {
			$(this).toggleClass("fa-eye fa-eye-slash");
			var input = $(".pass-input");
			if (input.attr("type") == "password") {
				input.attr("type", "text");
			} else {
				input.attr("type", "password");
			}
		});
	}
});


// Fancybox Config
$('[data-fancybox="gallery"]').fancybox({
	buttons: [
		"slideShow",
		"thumbs",
		"zoom",
		"fullScreen",
		"share",
		"close"
	],
	loop: false,
	protect: true
});

// Toggle full screen
function toggleFullScreen() {
	var a = $(window).height() - 10;
	if (!document.fullscreenElement && // alternative standard method
		!document.mozFullScreenElement && !document.webkitFullscreenElement) { // current working methods
		if (document.documentElement.requestFullscreen) {
			document.documentElement.requestFullscreen();
		} else if (document.documentElement.mozRequestFullScreen) {
			document.documentElement.mozRequestFullScreen();
		} else if (document.documentElement.webkitRequestFullscreen) {
			document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
		}
	} else {
		if (document.cancelFullScreen) {
			document.cancelFullScreen();
		} else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		} else if (document.webkitCancelFullScreen) {
			document.webkitCancelFullScreen();
		}
	}
	$('.full-screen').toggleClass('fa-expand');
	$('.full-screen').toggleClass('fa-compress');
}


// var swiper = new Swiper(".swiper", {
// 	// Optional parameters
// 	direction: "horizontal",
// 	loop: false,
// 	autoHeight: false,
// 	slidesPerView: 1,
//   // Responsive breakpoints
//   breakpoints: {
// 		640: {
//       slidesPerView:2,
// 			  spaceBetween: 40,
//     },
//     992: {
//       slidesPerView: 2,
// 			  spaceBetween: 40,
//     },
// 	1920: {
// 		slidesPerView: 2,
// 				spaceBetween: 40,
// 	  }
//   },

//   pagination: {
// 	el: '.swiper-pagination',
// 	clickable: true,
// },

// });

