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

bawkApp.controller('mainController', function($scope, $http, $location, $cookies, $timeout){

	var path = 'http://localhost:5000/';

	$scope.newPostInput = {text: ""}

	checkToken()

	if ($location.path() == '/' && $scope.loggedIn){
		loadPosts();

		getTrendingUsers();
	
	}

	function loadPosts(){
		$http.post('http://localhost:5000/get_posts', {
			username: $scope.username
		}).then(function success(response){
			$scope.posts = response.data;
			console.log($scope.posts)
		})	
	}

	function getTrendingUsers(){
		$http.post('http://localhost:5000/get_trending_users', {
			username: $scope.username
		}).then(function success(response){
			$scope.users = response.data;
			console.log($scope.users)

		})
	}


	$scope.register = function(){
		$http.post('http://localhost:5000/register_submit', {
			username: $scope.username,
			password: $scope.password,
			avatar: $scope.avatar
		}).then(function success(response){
			if(response.data == 'reg successful'){
				$scope.login();
				$('.dropdown.open .dropdown-toggle').dropdown('toggle');
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
			getTrendingUsers();
			loadPosts();
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
		newPostContent = $scope.newPostInput.text;
		console.log(newPostContent)
		// $scope.newPostInput = '';

		$http.post('http://localhost:5000/new_post', {
			newPostContent: newPostContent,
			username: $scope.username
		}).then(function success(response){
			$http.get('http://localhost:5000/get_posts', {

		}).then(function success(response){
			$scope.posts = response.data

			})
		})
		loadPosts();
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

		loadPosts();

	}

	$scope.vote = function(vid, voteType){
		if(voteType == true){
			var voteType = 1;
		}else if(voteType == false){
			var voteType = -1;
		}
		// console.log(vid);
		$http.post(path + 'process_vote', {
			vid: vid,
			voteType: voteType,
			username: $scope.username
		}).then(function successCallback(response){
			if(response.data == 'alreadyVoted'){
				$scope.alreadyVoted = true;
				$timeout(function(){
					$scope.alreadyVoted = false;
				}, 1500);
				console.log('alreadyVoted')
			}
			else if(response.data){
				// $scope.posts = response.data;
				loadPosts();
			}
		})


	}

	$scope.triggerSignUp = function() {
	    $timeout(function() {
	        angular.element('#sign-up-btn').trigger('click');
	    }, 100);
	};



})