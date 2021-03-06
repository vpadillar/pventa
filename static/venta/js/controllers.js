	var controllers = angular.module('controllers', []);

controllers.controller('order_controller', ['$scope', '$http', '$stateParams',
	function ($scope, $http, $stateParams) {
		$scope.search = "";
		$scope.order = {};
		$scope.total = 0;
		$scope.order_id = $stateParams.order_id;
		$scope.nocount = null;
		$scope.paid = false;
		$scope.table_selected = {
			table: 1
		};
		if ($scope.order_id){
			$scope.nocount = $scope.order_id;
			$http.get('/orders/'+ $scope.order_id + '/?format=json').success(function (data) {

				var order = data;
				for (var p in order.products){
					var product_obj = order.products[p];
					console.log(product_obj);
					var product = {
						'product' : product_obj.product,
						'product_name': product_obj.product_obj.name,
						'count': product_obj.count,
						'total_price': product_obj.product_obj.price * product_obj.count
					};
					$scope.order[product_obj.product] = product;
				}
				$scope.paid = data.paid;
				update_total();
			}).error(function(data){
				$scope.goTo('dashboard');
			});
			$http.get('/settable/?format=json&order_id=' + $scope.order_id).success(function(data){
				if (data[0]){
					$scope.table_selected = data[0];
				}
				console.log(data);
			});
			$http.get('/ws/aviable/tables/' + $scope.order_id + '/?format=json')
				.success(function (data) {
					$scope.tables = data;
			});
		}else{
			$http.get('/ws/nocount/').success(function(data){
				$scope.nocount = data;
			});
			$http.get('/tables/?format=json')
				.success(function (data) {
					$scope.tables = data;
			});
		}
		$scope.del = function(){
			var ok = confirm("¿Está seguro de borrar el elemento?");
			if (ok){
				var put = {
					'canceled': true
				};
				$http.put('/orders/' + $scope.order_id + '/', put).success(function (data){
					$scope.goTo("dashboard");
				});
			}
		};

		$scope.load_categorys = function (){
			$http.get('/categorys/?search=' + $scope.search)
				.success(function (data) {
					$scope.categorys = data;
			});


		};

		$scope.load_products = function (category){
			$http.get('/products/?format=json&category__id=' + category)
				.success(function (data) {
					$scope.products = data;
			});
		};

		$scope.minus_product = function (product_obj) {
			if ($scope.order[product_obj.id]){
				var count = $scope.order[product_obj.id]['count'];
				if (count <= 1){
					delete $scope.order[product_obj.id];
				}else {
					var product = {
						'product' : product_obj.id,
						'product_name': product_obj.name,
						'count': count - 1,
						'total_price':product_obj.price * (count - 1)
					};
					$scope.order[product_obj.id] = product;
				}
			}
			update_total();
		};

		$scope.plus_product = function (product_obj) {
			var count = 0;
			if ($scope.order[product_obj.id]){
				count = $scope.order[product_obj.id]['count'];
			}
			var product = {
				'product' : product_obj.id,
				'product_name': product_obj.name,
				'count': count + 1,
				'total_price':product_obj.price * (count + 1)
			};
			$scope.order[product_obj.id] = product;
			update_total();
		};

		function update_total(){
			$scope.total = 0;
			for (var i in $scope.order){
				$scope.total += $scope.order[i].total_price;
			}
		}
		$scope.print_order = function(success, error){
			/*try{
				var data = {
					"data": {"id": $scope.order_id + ""},
					"printer": "chef",
					"template": "order",
					"service": "order"
				};
				$http.post($scope.service.printer, data).success(function(){
	            	success(data);
	            }).error(function(data){
	            	error(data);
	            });
			}catch(e){
				alert(e);
			}*/
			success({});
		};
		$scope.pay = function(){
			var order = [];
			for (var i in $scope.order){
				order.push($scope.order[i]);
			}
			var post = {
				'csrfmiddlewaretoken': csrf,
				'products': order
			};

			if ($scope.order_id){
				$http.put('/orders/' + $scope.order_id + '/', post).success(function(data){
					$http.put('/settable/' + $scope.table_selected.id + '/', {
						'table': $scope.table_selected.table,
						'order': $scope.table_selected.order
					})
					.success(function(data){
						$scope.print_order(function(data) {
							$scope.goTo('confirm', {'order_id': $scope.order_id});
						}, function(data){
							alert("Ocurrió un error al intentar imprimir");
							$scope.goTo('orders_edit', {'order_id': $scope.order_id});
						});
					});
				});
			}else{
				$http.post('/orders/', post).success(function(order){
					console.log(order);
					$http.post('/settable/', {
						'table': $scope.table_selected.table,
						'order': order.id
					})
					.success(function(data){
						$scope.print_order(function(data) {
							//$scope.goTo('dashboard');
							$scope.goTo('confirm', {'order_id': order.id});
						}, function(data){
							alert("Ocurrió un error al intentar imprimir");
							$scope.goTo('orders_edit', {'order_id': order.id});
						});
					});
				});
			}
		};

		$scope.load_categorys();
	}
]);
controllers.controller('order_list_controller', ['$scope', '$http',
	function ($scope, $http) {
		$http.get('/orders/?paid=3').success(function (data) {
			$scope.orders = data;
		});
		$http.get('/pendant/?format=json')
			.success(function (data) {
				console.log(data);
				$scope.tables = data;
		});
	}
]);
controllers.controller('pay_list_controller', ['$scope', '$http',
	function ($scope, $http) {
		$http.get('/orders/?paid=3').success(function (data) {
			$scope.orders = data;
		});
		$http.get('/pendant/?format=json')
			.success(function (data) {
				console.log(data);
				$scope.tables = data;
		});
		$scope.paids = function(){
			$http.get('/orders/?paid=2').success(function (data) {
				$scope.orders = data;
			});
		};
		$scope.pending = function(){
			$http.get('/orders/?paid=3').success(function (data) {
				$scope.orders = data;
			});
		};
		$scope.all = function(){
			$http.get('/orders/').success(function (data) {
				$scope.orders = data;
			});
		};
	}
]);
controllers.controller('dashboard_controller', ['$scope', '$http',
	function ($scope, $http) {

	}
]);
controllers.controller('confirm_controller', ['$scope', '$http', '$stateParams',
	function ($scope, $http, $stateParams) {
		$scope.order_id = $stateParams.order_id;
		$scope.cash = 0;
		$scope.check = 0;
		$scope.card = 0;
		$scope.disscounts = 0;
		$scope.total = 0;
		$scope.subtotal = 0;
		$scope.total_paid = 0;
		$scope.checked = false;
		$scope.tip = 0;
		$scope.cc = "";
		$scope.name = "";
		$scope.tel = "";

		$http.get('/ws/config/').success(function (data) {
			$scope.conf = data;
			$http.get('/orders/?format=json&id=' + $scope.order_id).success(function (data) {
				$scope.order = data[0];

				for (var p in $scope.order.products){
					$scope.subtotal += $scope.order.products[p].count*$scope.order.products[p].product_obj.price;
				}
				$scope.tip = parseFloat(($scope.subtotal*$scope.conf.propina/100).toFixed(2));

				$scope.iva = $scope.subtotal*$scope.conf.iva/100;
				$scope.ipoconsumo = parseFloat(($scope.subtotal*$scope.conf.ipoconsumo/100).toFixed(2));
				$scope.update_total();
				if ($scope.order.paid){
					$http.get('/bills/' + $scope.order.bill + '/?format=json').success(function (data) {
						$scope.cash = parseFloat(data.cash);
						$scope.check = parseFloat(data.check);
						$scope.card = parseFloat(data.card);
						$scope.disscount = parseFloat(data.disscount);
						$scope.tip = parseFloat(data.tip);
						$scope.cc = data.cc;
						$scope.name = data.name;
						$scope.tel = data.tel;
						$scope.update_total();
						$scope.update_total_paid();
					});
				}
			});
		});

		$scope.clear = function(self){
			$scope.checked = false;
			if ($scope[self] == "0"){
				$scope[self] = "";
			}
		};
		$scope.fill = function(self){
			console.log($scope[self]);
			if ($scope[self] == "" || $scope[self] == null){
				$scope[self] = 0;
			}
		};
		$scope.update_total_paid = function(){
			$scope.total_paid = $scope.cash + $scope.check + $scope.card + $scope.disscounts;
		};
		$scope.update_total = function(){
			$scope.total = parseFloat(($scope.subtotal + $scope.iva + $scope.ipoconsumo + $scope.tip).toFixed(2));
		}
		$scope.checkin = function(){
			if ($scope.total_paid == $scope.total){
				$scope.checked = true;
			}else{
				total.setAttribute("ripple", "");
				window.setTimeout(function(){
					total.removeAttribute("ripple");
				}, 1000);
			}
		};
		$scope.get_client = function(){
			$http.get('/clients/?cc=' + $scope.cc).success(function (data) {
				if (data[0]){
					$scope.name = data[0].name;
					$scope.tel = data[0].tel;
				}
			});
		};
		$scope.print_bill = function(success, error){
			try{
				var data = {
					"data": {"id": $scope.order.bill + ""},
					"printer": "bill",
					"template": "bill",
					"service": "bill"
				};
				alert($scope.service.printer);
				$http.post($scope.service.printer, data).success(function(){
	            	success(data);
	            }).error(function(data){
	            	error(data);
	            });
			}catch(e){
				alert(e);
			}
		};
		$scope.pv_print = function(){
			$scope.print_bill(function(data){
				window.location.reload();
			}, function(data){
				alert("Ocurrió un error al intentar imprimir");
			});
		}
		$scope.save = function(){
			if (!$scope.checked || $scope.total_paid != $scope.total){
				var total = document.getElementById("total");

				total.setAttribute("ripple", "");
				window.setTimeout(function(){
					total.removeAttribute("ripple");
				}, 1000);

				return;
			}
			var products = $scope.order.products;
			var total = 0;
			for (var i in products){
				products[i].total_price = (products[i].count*products[i].product_obj.price).toFixed(2);
				total += products[i].price;
			}
			$scope.totaltip = $scope.total + $scope.tip;
			alert($scope.order.waiter);
			var post = {
				'csrfmiddlewaretoken': csrf,
				'cash': $scope.cash,
				'check': $scope.check,
				'card': $scope.card,
				'disscounts': $scope.disscounts,
				'products': JSON.stringify(products),
				'cc': $scope.cc,
				'name': $scope.name,
				'tel':$scope.tel,
				'tip': $scope.tip,
				'casher': 'no-set',
				'waiter': $scope.order.waiter,
				'subtotal': $scope.subtotal,
				'iva': $scope.iva,
				'ipoconsumo': $scope.ipoconsumo,
				'total': $scope.total,
				'totaltip': $scope.totaltip
			};
			$http.post('/bills/', post).success(function (data) {
				var put = {
					'bill': data.id,
				    "paid": true
				};
				$http.put('/orders/' + $scope.order_id + '/', put)
					.success(function(data){
						$scope.order = data;
						$scope.pv_print();
				});
			});
		};
	}
]);
controllers.controller('product_list_controller', ['$scope', '$http',
	function ($scope, $http) {
		$scope.search = "";
		$scope.load_categorys = function (){
			$http.get('/categorys/?format=json&search=' + $scope.search)
			.success(function (data) {
				$scope.categorys = data;
			});
		};
		$scope.load_products = function (category_id, category_name){
			$scope.category_name = category_name;
			$http.get('/products/?format=json&category__id=' + category_id)
				.success(function (data) {
					$scope.products = data;
			});
		};
		$scope.load_categorys();

	}
]);
controllers.controller('category_list_controller', ['$scope', '$http',
	function ($scope, $http) {
		$scope.search = "";
		$scope.load_categorys = function (){
			$http.get('/categorys/?format=json&search=' + $scope.search).success(function (data) {
				$scope.categorys = data;
			});
		};
		$scope.load_categorys();

	}
]);

function default_crud_controller($scope, $http, $stateParams, object_name, attributes, url, new_label, object_label){
	$scope[object_name + '_id'] = $stateParams[object_name + '_id'];
	function init_callback(callback){
		if ($scope[object_name + '_id']){
			$scope.title = object_label + " #" + $scope[object_name + '_id'];
			$scope.button = "create";
			$http.get(url + $scope[object_name + '_id'] + '/').success(function(data){
				callback(data);
			}).error(function(data){
				$scope.goTo("dashboard");
			});
		}else{
			$scope.title = new_label + " " + object_label;
			$scope.button = "add";
			callback();
		}
	}
	function init_list(index, data_callback){

		$http.get(attributes[index]['url'])
			.success(function(data){
				$scope[object_name + '_' + index] = {};
				$scope[object_name + '_' + index].data = {
			    	availableOptions: data,
					selectedOption: {}
			    };
				if (data_callback){
					for (var i in $scope[object_name + '_' + index].data.availableOptions){
						if ($scope[object_name + '_' + index].data.availableOptions[i].id == data_callback[index]){
							$scope[object_name + '_' + index].data.selectedOption = $scope[object_name + '_' + index].data.availableOptions[i];
							return;
						}
					}
				}
			});
	}
	function init(){
		init_callback(function (data){
			for (var i in attributes){
				if (attributes[i] == 'value'){
					$scope[object_name + '_' + i] = (data?data[i]:"");
				}else
				if (attributes[i] == 'float'){
					$scope[object_name + '_' + i] = (data? parseFloat(data[i]):0);
				}else
				if (attributes[i]['type'] == 'list'){
					init_list(i, data);
				}
			}
		});
	}
	init();
	$scope.del = function(){
		var ok = confirm("¿Está seguro de borrar el elemento?");
		if (ok){
			$http.delete(url + $scope[object_name + '_id'] + '/').success(function (data){
				goTo("dashboard");
			});
		}
	};
	$scope.send = function(){
		var post = {
			'csrfmiddlewaretoken': csrf
		};
		for (var i in attributes){
			if (attributes[i] == 'value'){
				post[i] = $scope[object_name + '_' + i];
			}else
			if (attributes[i] == 'float'){
				post[i] = $scope[object_name + '_' + i];
			}else
			if (attributes[i]['type'] == 'list'){
				post[i] = $scope[object_name + '_' + i].data.selectedOption['id'];
			}
		}
		var send;
		if ($scope[object_name + '_id']){
			post['id'] = $scope[object_name + '_id'];
			send = $http.put(url + $scope[object_name + '_id'] + '/', post);
		}else{
			send = $http.post(url, post);
		}

		send.success(function (data){
			if (!$scope[object_name + '_id']){
				for (var i in attributes){
					if (attributes[i] == 'value' ){
						$scope[object_name + '_' + i] = "";
					}else
					if (attributes[i] == 'float' ){
						$scope[object_name + '_' + i] = 0;
					}else
					if (attributes[i]['type'] == 'list'){
						$scope[object_name + '_' + i].data.selectedOption = {};
					}
				}
			}
			var success = document.getElementById("success");

			success.setAttribute("appear", "");
			window.setTimeout(function(){
				success.removeAttribute("appear");
			}, 1500);
		}).error(function (data){
			var button = document.getElementById("add-button");
			var form = document.getElementById("form");

			button.setAttribute("ripple", "");
			form.setAttribute("show", "");
			window.setTimeout(function(){
				button.removeAttribute("ripple");
			}, 1000);
		});
	};
}

controllers.controller('category_controller', ['$scope', '$http', '$stateParams',
	function ($scope, $http, $stateParams) {
		default_crud_controller($scope, $http, $stateParams,
				'category', {
					'name': 'value',
					'image': {
						'type': 'list',
						'url': '/images/?format=json'
					}
				}, '/categorys/', 'Nueva', 'Categoría'
			);
	}
]);

controllers.controller('product_controller', ['$scope', '$http', '$stateParams',
	function ($scope, $http, $stateParams) {
		default_crud_controller($scope, $http, $stateParams,
				'product', {
					'name': 'value',
					'price': 'float',
					'presentation': {
						'type': 'list',
						'url': '/presentation/?format=json'
					},
					'category': {
						'type': 'list',
						'url': '/categorys/?format=json'
					}
				}, '/products/', 'Nuevo', 'Producto'
			);
	}
]);
controllers.controller('login_controller', ['$scope', '$http',
	function ($scope, $http) {
		$scope.username = "";
		$scope.password = "";

		$scope.login = function(){
			var post = {
				'csrfmiddlewaretoken': csrf,
				'username': $scope.username,
				'password': $scope.password
			};

			$http.post('/auth/login/', post).success(function (data){
				window.location = "/";
			}).error(function(data){
				var button = document.getElementById("login-button");
				var message = document.getElementById("message");

				button.setAttribute("ripple", "");
				message.removeAttribute("hide");
				window.setTimeout(function(){
					button.removeAttribute("ripple");
				}, 1000);
			});
		}
	}
]);
