/**
* @name: Venta JS
*
**/
var venta_app = angular.module('venta_app', [
	'ui.router',
	'ngRoute',
	'controllers'
]);

venta_app.controller('main_controller',function($scope, $http, $state){
	var menu = document.getElementById("menu");
	$http.get('/ws/service/').success(function (data){
		console.log(data);
		$scope.service = data;
	});
	$scope.goTo = function(url, data){
		$state.go(url, data);
	};
	$scope.logout = function(url, data){
		$http.delete('/ws/login/').success(function(){
			window.location = "";
		});
	};
	function menu_magic(){
		if (window.location.hash === "#/"){
			menu.setAttribute("style", "display: none;");
		}else{
			menu.removeAttribute("style");
		}
	}
	window.addEventListener('hashchange', function() {
		menu_magic();
	});
	menu_magic();
});

venta_app.config(function($interpolateProvider, $httpProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

var login_app = angular.module('login_app', [
	'controllers'
]);

login_app.config(function($interpolateProvider, $httpProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
