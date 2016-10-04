var bawkApp = angular.module('bawkApp', ['ngRoute', 'ngCookies'], function($interpolateProvider){
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
})

bawkApp.config(function($locationProvider) {
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
});

bawkApp.controller('mainController', function($scope, $http, $location, $cookies){

	checkToken()

	if ($location.path() == '/'){
		$http.get('http://localhost:5000/get_posts', {

		}).then(function success(response){
			$scope.posts = response.data
			// console.log($scope.posts)
		})
	
	}


	$scope.register = function(){
		$http.post('http://localhost:5000/register_submit', {
			username: $scope.username,
			password: $scope.password,
			email: $scope.email

		})
		console.log('register')
	}

	$scope.login = function(){
		$http.post('http://localhost:5000/login_submit', {
			username: $scope.username,
			password: $scope.password
		}).then(function successCallback(response){
			if (response.data == "true"){
				$scope.loggedIn = true;
				$scope.signedInAs = $scope.username;
				$cookies.put('username', $scope.username);
			}
		})
	}

	function checkToken() {
		if($cookies.get('username')) {
			$scope.username = $cookies.get('username');
			$scope.loggedIn = true;
			$scope.signedInAs = $scope.username;
			$http.post('http://localhost:5000/')	
		}
	}

	$scope.logout = function(){
		$cookies.remove('token');
		$scope.signedInAs = null;
		$scope.loggedIn = false;
	}



})