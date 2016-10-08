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

	// auto resize text area
	// found @ http://stackoverflow.com/questions/23818131/dynamically-expand-height-of-input-type-text-based-on-number-of-characters-typ
	var span = $('<span>').css('display', 'inline-block')
	    .css('word-break', 'break-all')
	    .appendTo('body').css('visibility', 'hidden');
	function initSpan(textarea) {
	    span.text(textarea.text())
	        .width(textarea.width())
	        .css('font', textarea.css('font'));
	}
	$('textarea').on({
	    input: function() {
	        var text = $(this).val();
	        span.text(text);
	        $(this).height(text ? span.height() : '1.1em');
	    },
	    focus: function() {
	        initSpan($(this));
	    },
	    keypress: function(e) {
	        //cancel the Enter keystroke, otherwise a new line will be created
	        //This ensures the correct behavior when user types Enter 
	        //into an input field
	        if (e.which == 13) e.preventDefault();
	    }
	});


	checkToken()



	if ($location.path() == '/'){
		// load posts
		$http.post('http://localhost:5000/get_posts', {
			username: $scope.username
		}).then(function success(response){
			$scope.posts = response.data;

		})
		// get trending users
		$http.post('http://localhost:5000/get_trending_users', {
			username: $scope.username
		}).then(function success(response){
			$scope.users = response.data;

		})
	
	}


	$scope.register = function(){
		$http.post('http://localhost:5000/register_submit', {
			username: $scope.username,
			password: $scope.password,
			avatar: $scope.avatar
		}).then(function success(response){
			if(response.data == 'reg successful'){
				$scope.loggedIn = true;
			}
		})

	}

	$scope.login = function(){
		$http.post('http://localhost:5000/login_submit', {
			username: $scope.username,
			password: $scope.password
		}).then(function successCallback(response){
			if (response.data){
				$scope.loggedIn = true;
				$scope.signedInAs = $scope.username;
				$cookies.put('username', $scope.username);
				$scope.avatar = response.data;
				$cookies.put('avatar', $scope.avatar)
			}
		})
	}

	function checkToken() {
		if($cookies.get('username')) {
			$scope.username = $cookies.get('username');
			$scope.avatar = $cookies.get('avatar');
			$scope.loggedIn = true;
			$scope.signedInAs = $scope.username;
			// $http.post('http://localhost:5000/')	
		}
	}

	$scope.logout = function(){
		$cookies.remove('username');
		$cookies.remove('avatar');
		$scope.signedInAs = null;
		$scope.loggedIn = false;
	}

	$scope.makePost = function(){
		newPostContent = $scope.newPostInput;
		$scope.newPostInput = '';

		$http.post('http://localhost:5000/new_post', {
			newPostContent: newPostContent,
			username: $scope.username
		}).then(function success(response){
			$http.get('http://localhost:5000/get_posts', {

			}).then(function success(response){
			$scope.posts = response.data

			})
		})
	}

	$scope.follow = function(){
		// $http.post('http://localhost:5000/follow', {
		// 	username: $scope.username,

		// })
	}

	$scope.followUser = function(id, index){
		$scope.users.splice(index, 1)
		if ($scope.users.length == 0){
			$scope.everyoneFollowed = true;
		}
		console.log(id)

		$http.post('http://localhost:5000/follow', {
			username: $scope.username,
			following_id: id
		})

	}



})