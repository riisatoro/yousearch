var display_menu = false

function menu_request() {
	if (display_menu) {
		$(".hidden-menu-list").hide()
		display_menu = false
	}
	else {
		$(".hidden-menu-list").show()
		display_menu = true
	}
}

$(".menu-img").click(menu_request);
