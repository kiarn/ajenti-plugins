angular.module('session_list').controller 'SessionListIndexController', ($scope, $http, $interval, $timeout, notify, pageTitle, messagebox, gettext, config) ->
    pageTitle.set(gettext('List all sessions'))
    
    $http.get('/api/session_list/list').then (resp) ->
        $scope.sessions = resp.data
        for session in $scope.sessions
            session.date = new Date(session.timestamp)
        $scope.number = Object.keys($scope.sessions).length
        $scope.session_max_time = config.data.session_max_time
