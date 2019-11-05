angular.module('extra_certificates').config($routeProvider => {
    $routeProvider.when('/view/lm/certificates', {
        templateUrl: '/extra_certificates:resources/partial/index.html',
        controller: 'CertIndexController'
    })
});
