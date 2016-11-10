/**
* @name: Venta JS
* 
**/

venta_app.config(['$stateProvider', '$urlRouterProvider','$locationProvider', '$httpProvider',
    function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider){
		$stateProvider.
			state('dashboard', {
				url: '/',
				templateUrl: 'dashboard.html',
				controller: 'dashboard_controller'
			}).
			state('orders_add', {
				url: '/order/add',
				templateUrl: 'order_add.html',
				controller: 'order_controller'
			}).
			state('orders_edit', {
				url: '/order/edit/:order_id',
				templateUrl: 'order_add.html',
				controller: 'order_controller'
			}).
			state('orders', {
				url: '/order/list',
				templateUrl: 'order_list.html',
				controller: 'order_list_controller'
			})
			.state('pay', {
				url: '/pay/list',
				templateUrl: 'pay_list.html',
				controller: 'pay_list_controller'
			}).
			state('confirm', {
				url: '/confirm/:order_id',
				templateUrl: 'confirm.html',
				controller: 'confirm_controller'
			}).
			state('categories', {
				url: '/category/list',
				templateUrl: 'category_list.html',
				controller: 'category_list_controller'
			}).
			state('categories_add', {
				url: '/category/add',
				templateUrl: 'category_add.html',
				controller: 'category_controller'
			}).
			state('categories_edit', {
				url: '/category/edit/:category_id',
				templateUrl: 'category_add.html',
				controller: 'category_controller'
			}).
			state('products', {
				url: '/product/list',
				templateUrl: 'product_list.html',
				controller: 'product_list_controller'
			}).
			state('product_add', {
				url: '/product/add',
				templateUrl: 'product_add.html',
				controller: 'product_controller'
			}).
			state('product_edit', {
				url: '/product/edit/:product_id',
				templateUrl: 'product_add.html',
				controller: 'product_controller'
			});
			$urlRouterProvider.otherwise('/');
	}
]);