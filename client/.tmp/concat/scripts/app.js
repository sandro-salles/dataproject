'use strict';

/**
 * @ngdoc overview
 * @name CONTACTPRO
 * @description
 * # CONTACTPRO
 *
 * Main module of the application.
 */

/*jshint -W079 */

var app = angular
    .module('CONTACTPRO', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngSanitize',
        'ngTouch',
        'ngMessages',
        'picardy.fontawesome',
        'ui.bootstrap',
        'ui.router',
        'ui.utils',
        'angular-loading-bar',
        'angular-momentjs',
        'jcs-autoValidate',
        'FBAngular',
        'toastr',
        'angularBootstrapNavTree',
        'oc.lazyLoad',
        'ui.select',
        'ui.tree',
        'ui.gravatar',
        'textAngular',
        'angular-flot',
        'angular-rickshaw',
        'easypiechart',
        'ui.calendar',
        'ngTagsInput',
        'ngMaterial',
        'localytics.directives',
        'angular-intro',
        'dragularModule',
        'djangoRESTResources',
        'angular-jwt',
        'ngCpfCnpj',
        'dynamicNumber'
    ])
    .run(['$rootScope', '$state', '$stateParams', '$location', '$cookieStore', '$http', 'jwtHelper', 'bootstrap3ElementModifier', 'AuthService', function($rootScope, $state, $stateParams, $location, $cookieStore, $http, jwtHelper, bootstrap3ElementModifier, AuthService) {

        bootstrap3ElementModifier.enableValidationStateIcons(true);

        $rootScope.globals = $cookieStore.get('globals') || {};

        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'JWT ' + $rootScope.globals.currentUser.token; // jshint ignore:line
        }

        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $rootScope.$on('$stateChangeSuccess', function(event, toState) {

            event.targetScope.$watch('$viewContentLoaded', function() {

                angular.element('html, body, #content').animate({
                    scrollTop: 0
                }, 200);

                setTimeout(function() {
                    angular.element('#wrap').css('visibility', 'visible');

                    if (!angular.element('.dropdown').hasClass('open')) {
                        angular.element('.dropdown').find('>ul').slideUp();
                    }
                }, 200);
            });
            $rootScope.containerClass = toState.containerClass;
        });

        var checkUserSession = function(next, current) {

            var public_states = ['/core/login/', '/core/forgotpass/', '/core/forgotpass/success/'];
            var restricted = true;
            var current_path = $location.path();
            
            for (var pstate in public_states) {
                if (current_path.indexOf(public_states[pstate]) > -1) {
                    restricted = false;
                    break;
                }
            }

            var loggedIn = $rootScope.globals.currentUser;
            if (restricted && (!loggedIn || jwtHelper.isTokenExpired(loggedIn.token))) {
                
                AuthService.ClearCredentials();

                if (current_path) {
                    $location.path('/core/login/').search('origin', encodeURIComponent(current_path));    
                } else {
                    $location.path('/core/login/');
                }
                
            }
        };

        $rootScope.$on('$locationChangeStart', function(event, next, current) {
            checkUserSession(next, current);
        });

        $rootScope.$on('$stateChangeStart', function(event, next, current) {
            checkUserSession(next, current);
        });

        $rootScope.Logout = function() {
            AuthService.ClearCredentials();
            $location.path('/core/login/');
        }

    }])
    .config(['uiSelectConfig', function(uiSelectConfig) {
        uiSelectConfig.theme = 'bootstrap';
    }])
    .config(["$resourceProvider", function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
    .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/app/dashboard');

        $stateProvider

        //app core pages (errors, login,signup)
            .state('core', {
                abstract: true,
                url: '/core',
                template: '<div ui-view></div>',
                authenticated: false
            })
            .state('core.login', {
                url: '/login/?origin',
                controller: 'LoginCtrl',
                templateUrl: 'views/tmpl/login.html'
            })
            .state('core.forgotpass', {
                url: '/forgotpass',
                controller: 'ForgotPasswordCtrl',
                templateUrl: 'views/tmpl/forgotpass.html'
            })
            .state('core.forgotpass-success', {
                url: '/forgotpass/success',
                controller: 'ForgotPasswordSuccessCtrl',
                templateUrl: 'views/tmpl/forgotpass-success.html'
            })


        .state('app', {
            abstract: true,
            url: '/app',
            templateUrl: 'views/tmpl/app.html',
            authenticated: true
        })

        //dashboard
        .state('app.dashboard', {
            url: '/dashboard',
            controller: 'DashboardCtrl',
            templateUrl: 'views/tmpl/dashboard.html',
        })

        //explorer
        .state('app.purchase', {
            url: '/purchase',
            controller: 'PurchaseCtrl',
            templateUrl: 'views/tmpl/purchase.html',
            containerClass: 'sidebar-xs-forced sidebar-xs'
        })

        //explorer
        .state('app.corporation', {
            url: '/corporation',
            controller: 'CorporationCtrl',
            templateUrl: 'views/tmpl/corporation.html',
            containerClass: 'sidebar-xs-forced sidebar-xs'
        })

        //explorer
        .state('app.collections', {
                url: '/collections',
                controller: 'CollectionsCtrl',
                templateUrl: 'views/tmpl/collections.html',
                containerClass: 'sidebar-xs-forced sidebar-xs'
            })
            //explorer
            .state('app.collections.navigator', {
                url: '/collections/navigator',
                controller: 'NavigatorCtrl',
                templateUrl: 'views/tmpl/collections.html',
                containerClass: 'sidebar-xs-forced sidebar-xs'
            });
    }]);

'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('MainCtrl', ["$scope", "$http", function ($scope, $http) {

    $scope.main = {
      title: 'CONTACTPRO',
      settings: {
        navbarHeaderColor: 'scheme-default',
        sidebarColor: 'scheme-default',
        brandingColor: 'scheme-default',
        activeColor: 'default-scheme-color',
        headerFixed: true,
        asideFixed: true,
        rightbarShow: false
      }
    };

    $scope.ajaxFaker = function(){
      $scope.data=[];
      var url = 'http://www.filltext.com/?rows=10&fname={firstName}&lname={lastName}&delay=5&callback=JSON_CALLBACK';

      $http.jsonp(url).success(function(data){
        $scope.data=data;
        angular.element('.tile.refreshing').removeClass('refreshing');
      });
    };

    $scope.changeLanguage = function (langKey) {
    };

  }]);

'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:navCollapse
 * @description
 * # navCollapse
 * # sidebar navigation dropdown collapse
 */
app
  .directive('navCollapse', ["$timeout", function ($timeout) {
    return {
      restrict: 'A',
      link: function($scope, $el) {

        $timeout(function(){

          var $dropdowns = $el.find('ul').parent('li'),
            $a = $dropdowns.children('a'),
            $notDropdowns = $el.children('li').not($dropdowns),
            $notDropdownsLinks = $notDropdowns.children('a'),
            app = angular.element('.appWrapper'),
            sidebar = angular.element('#sidebar'),
            controls = angular.element('#controls');

          $dropdowns.addClass('dropdown');

          var $submenus = $dropdowns.find('ul >.dropdown');
          $submenus.addClass('submenu');

          $a.append('<i class="fa fa-plus"></i>');

          $a.on('click', function(event) {
            if (app.hasClass('sidebar-sm') || app.hasClass('sidebar-xs') || app.hasClass('hz-menu')) {
              return false;
            }

            var $this = angular.element(this),
              $parent = $this.parent('li'),
              $openSubmenu = angular.element('.submenu.open');

            if (!$parent.hasClass('submenu')) {
              $dropdowns.not($parent).removeClass('open').find('ul').slideUp();
            }

            $openSubmenu.not($this.parents('.submenu')).removeClass('open').find('ul').slideUp();
            $parent.toggleClass('open').find('>ul').stop().slideToggle();
            event.preventDefault();
          });

          $dropdowns.on('mouseenter', function() {
            sidebar.addClass('dropdown-open');
            controls.addClass('dropdown-open');
          });

          $dropdowns.on('mouseleave', function() {
            sidebar.removeClass('dropdown-open');
            controls.removeClass('dropdown-open');
          });

          $notDropdownsLinks.on('click', function() {
            $dropdowns.removeClass('open').find('ul').slideUp();
          });

          var $activeDropdown = angular.element('.dropdown>ul>.active').parent();

          $activeDropdown.css('display', 'block');
        });

      }
    };
  }]);

'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:slimScroll
 * @description
 * # slimScroll
 */
app
  .directive('slimscroll', function () {
    return {
      restrict: 'A',
      link: function ($scope, $elem, $attr) {
        var off = [];
        var option = {};

        var refresh = function () {
          if ($attr.slimscroll) {
            option = $scope.$eval($attr.slimscroll);
          } else if ($attr.slimscrollOption) {
            option = $scope.$eval($attr.slimscrollOption);
          }

          angular.element($elem).slimScroll({ destroy: true });

          angular.element($elem).slimScroll(option);
        };

        var registerWatch = function () {
          if ($attr.slimscroll && !option.noWatch) {
            off.push($scope.$watchCollection($attr.slimscroll, refresh));
          }

          if ($attr.slimscrollWatch) {
            off.push($scope.$watchCollection($attr.slimscrollWatch, refresh));
          }

          if ($attr.slimscrolllistento) {
            off.push($scope.$on($attr.slimscrolllistento, refresh));
          }
        };

        var destructor = function () {
          angular.element($elem).slimScroll({ destroy: true });
          off.forEach(function (unbind) {
            unbind();
          });
          off = null;
        };

        off.push($scope.$on('$destroy', destructor));

        registerWatch();
      }
    };
  });

'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:SparklineCtrl
 * @description
 * # sparklineCtrl navbar
 * Controller of the CONTACTPRO
 */
app
  .controller('SparklineCtrl', ["$scope", function ($scope) {
    $scope.navChart1 = {
      data: [5, 8, 3, 4, 6, 2, 1, 9, 7],
      options: {
        type: 'bar',
        barColor: '#92424e',
        barWidth: '6px',
        height: '36px'
      }
    };
    $scope.navChart2 = {
      data: [2, 4, 5, 3, 8, 9, 7, 3, 5],
      options: {
        type: 'bar',
        barColor: '#397193',
        barWidth: '6px',
        height: '36px'
      }
    };
  }]);

'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:sparkline
 * @description
 * # sparkline
 */
app
  .directive('sparkline', [
  function() {
    return {
      restrict: 'A',
      scope: {
        data: '=',
        options: '='
      },
      link: function($scope, $el) {
        var data = $scope.data,
            options = $scope.options,
            chartResize,
            chartRedraw = function() {
              return $el.sparkline(data, options);
            };
        angular.element(window).resize(function() {
          clearTimeout(chartResize);
          chartResize = setTimeout(chartRedraw, 200);
        });
        return chartRedraw();
      }
    };
  }
]);

'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('DashboardCtrl', ["$scope", "$http", function($scope,$http){
    $scope.page = {
      title: 'Dashboard',
      subtitle: ''
    };

    $scope.getUsers = function(){
      $scope.data=[];
      var url = 'http://www.filltext.com/?rows=10&fname={firstName}&lname={lastName}&delay=3&callback=JSON_CALLBACK';

      $http.jsonp(url).success(function(data){
          $scope.data=data;
      });
    };

    $scope.getUsers();
  }])

  .controller('StatisticsChartCtrl', ["$scope", function ($scope) {

    $scope.dataset = [{
      data: [[1,15],[2,40],[3,35],[4,39],[5,42],[6,50],[7,46],[8,49],[9,59],[10,60],[11,58],[12,74]],
      label: 'Unique Visits',
      points: {
        show: true,
        radius: 4
      },
      splines: {
        show: true,
        tension: 0.45,
        lineWidth: 4,
        fill: 0
      }
    }, {
      data: [[1,50],[2,80],[3,90],[4,85],[5,99],[6,125],[7,114],[8,96],[9,130],[10,145],[11,139],[12,160]],
      label: 'Page Views',
      bars: {
        show: true,
        barWidth: 0.6,
        lineWidth: 0,
        fillColor: { colors: [{ opacity: 0.3 }, { opacity: 0.8}] }
      }
    }];

    $scope.options = {
      colors: ['#e05d6f','#61c8b8'],
      series: {
        shadowSize: 0
      },
      legend: {
        backgroundOpacity: 0,
        margin: -7,
        position: 'ne',
        noColumns: 2
      },
      xaxis: {
        tickLength: 0,
        font: {
          color: '#fff'
        },
        position: 'bottom',
        ticks: [
          [ 1, 'JAN' ], [ 2, 'FEB' ], [ 3, 'MAR' ], [ 4, 'APR' ], [ 5, 'MAY' ], [ 6, 'JUN' ], [ 7, 'JUL' ], [ 8, 'AUG' ], [ 9, 'SEP' ], [ 10, 'OCT' ], [ 11, 'NOV' ], [ 12, 'DEC' ]
        ]
      },
      yaxis: {
        tickLength: 0,
        font: {
          color: '#fff'
        }
      },
      grid: {
        borderWidth: {
          top: 0,
          right: 0,
          bottom: 1,
          left: 1
        },
        borderColor: 'rgba(255,255,255,.3)',
        margin:0,
        minBorderMargin:0,
        labelMargin:20,
        hoverable: true,
        clickable: true,
        mouseActiveRadius:6
      },
      tooltip: true,
      tooltipOpts: {
        content: '%s: %y',
        defaultTheme: false,
        shifts: {
          x: 0,
          y: 20
        }
      }
    };
  }])

  .controller('ActualStatisticsCtrl',["$scope", function($scope){
    $scope.easypiechart = {
      percent: 100,
      options: {
        animate: {
          duration: 3000,
          enabled: true
        },
        barColor: '#418bca',
        scaleColor: false,
        lineCap: 'round',
        size: 140,
        lineWidth: 4
      }
    };
    $scope.easypiechart2 = {
      percent: 75,
      options: {
        animate: {
          duration: 3000,
          enabled: true
        },
        barColor: '#e05d6f',
        scaleColor: false,
        lineCap: 'round',
        size: 140,
        lineWidth: 4
      }
    };
    $scope.easypiechart3 = {
      percent: 46,
      options: {
        animate: {
          duration: 3000,
          enabled: true
        },
        barColor: '#16a085',
        scaleColor: false,
        lineCap: 'round',
        size: 140,
        lineWidth: 4
      }
    };
  }])

  .controller('BrowseUsageCtrl', ["$scope", function ($scope) {

    $scope.donutData = [
      {label: 'Chrome', value: 25, color: '#00a3d8'},
      {label: 'Safari', value: 20, color: '#2fbbe8'},
      {label: 'Firefox', value: 15, color: '#72cae7'},
      {label: 'Opera', value: 5, color: '#d9544f'},
      {label: 'Internet Explorer', value: 10, color: '#ffc100'},
      {label: 'Other', value: 25, color: '#1693A5'}
    ];

    $scope.oneAtATime = true;

    $scope.status = {
      isFirstOpen: true,
      tab1: {
        open: true
      },
      tab2: {
        open: false
      },
      tab3: {
        open: false
      }
    };

  }])

  .controller('RealtimeLoadCtrl', ["$scope", "$interval", function($scope, $interval){

    $scope.options1 = {
      renderer: 'area',
      height: 133
    };

    $scope.seriesData = [ [], []];
    var random = new Rickshaw.Fixtures.RandomData(50);

    for (var i = 0; i < 50; i++) {
      random.addData($scope.seriesData);
    }

    var updateInterval = 800;

    $interval(function() {
      random.removeData($scope.seriesData);
      random.addData($scope.seriesData);
    }, updateInterval);

    $scope.series1 = [{
      name: 'Series 1',
      color: 'steelblue',
      data: $scope.seriesData[0]
    }, {
      name: 'Series 2',
      color: 'lightblue',
      data: $scope.seriesData[1]
    }];

    $scope.features1 = {
      hover: {
        xFormatter: function(x) {
          return new Date(x * 1000).toUTCString();
        },
        yFormatter: function(y) {
          return Math.floor(y) + '%';
        }
      }
    };
  }])


'use strict';

if (!Object.keys) {
    Object.keys = function (obj) {
        var keys = [],
            k;
        for (k in obj) {
            if (Object.prototype.hasOwnProperty.call(obj, k)) {
                keys.push(k);
            }
        }
        return keys;
    };
}

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:ExplorerCtrl
 * @description
 * # ExplorerCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('PurchaseCtrl', 
        ['$scope', '$http', 'Cart', 'Criteria', 'State', 'Carrier', 'Areacode', 'City', 'Neighborhood', 
        function($scope, $http, Cart, Criteria, State, Carrier, Areacode, City, Neighborhood) {
            $scope.page = {
                title: 'Comprar coleção de registros',
                subtitle: ''
            };

            $scope.counting = false;
            $scope.updating = false;
            $scope.CHECKOUT = 'checkout';
            $scope.MATCH = 'match';
            $scope.PACK = 'pack';

            $scope.filter = {
                nature: '',
                state: '',
                carrier: '',
                areacode: '',
                city: '',
                neighborhood: '',
                zipcode: ''
            };

            $scope.cart = Cart.query();

            $scope.natures = [{
                id: 'P',
                name: 'Pessoa Física'
            }, {
                id: 'L',
                name: 'Pessoa Jurídica'
            }];

            $scope.states = [];
            $scope.carriers = [];
            $scope.areacodes = [];
            $scope.cities = [];
            $scope.neighborhoods = [];
            $scope.zipcodes = [];

            $scope.count = 0;

            $scope.modality = null;

            $scope.addCriteria = function() {
                $scope.cart = Criteria.save({}, $scope.filter)
            }

            $scope.deleteCriteria = function(criteria_id) {
                $scope.cart = Criteria.delete({}, {id: criteria_id})

                if (!$scope.cart.count) {
                    steps.step2 = true;
                }
            }

            $scope.updateStates = function() {

                $scope.filter.state, $scope.filter.carrier, $scope.filter.areacode, $scope.filter.city, $scope.filter.neighborhood = '';  
                    
                $scope.states = [];
                $scope.carriers = [];
                $scope.areacodes = [];
                $scope.cities = [];
                $scope.neighborhoods = [];

                if ($scope.filter.nature) {

                    $scope.states = State.query({
                        nature: $scope.filter.nature
                    });

                    $scope.states.$promise.then(function(result) {
                        $scope.states = result;

                        $scope.updateCount();
                    });

                } else {
                    $scope.updateCount();
                }
            }

            $scope.updateCarriers = function() {

                $scope.filter.carrier, $scope.filter.areacode, $scope.filter.city, $scope.filter.neighborhood = '';  
                
                $scope.carriers = [];
                $scope.areacodes = [];
                $scope.cities = [];
                $scope.neighborhoods = [];

                if ($scope.filter.state) {

                    $scope.carriers = Carrier.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state
                    });

                    $scope.carriers.$promise.then(function(result) {
                        $scope.carriers = result;
                        $scope.updateCount();
                    });

                } else {
                    $scope.updateCount();
                }
            }

            $scope.updateAreacodes = function() {

                if ($scope.filter.carrier) {

                    $scope.filter.areacode, $scope.filter.city, $scope.filter.neighborhood = '';  
                    
                    $scope.areacodes = [];
                    $scope.cities = [];
                    $scope.neighborhoods = [];

                    $scope.areacodes = Areacode.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state,
                        carrier: $scope.filter.carrier
                    });

                    $scope.areacodes.$promise.then(function(result) {
                        $scope.areacodes = result;

                        $scope.updateCount();
                    });

                }
            }

            $scope.updateCities = function() {

                if ($scope.filter.areacode) {

                    $scope.filter.city, $scope.filter.neighborhood = '';  
                    
                    $scope.cities = [];
                    $scope.neighborhoods = [];

                    $scope.cities = City.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state,
                        carrier: $scope.filter.carrier,
                        areacode: $scope.filter.areacode
                    });

                    $scope.cities.$promise.then(function(result) {
                        $scope.cities = result;
                        $scope.updateCount();
                    });

                }

            }

            $scope.updateNeighborhoods = function() {

                if ($scope.filter.city) {

                    $scope.filter.neighborhood = '';  
                    
                    $scope.neighborhoods = [];


                    $scope.neighborhoods = Neighborhood.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state,
                        carrier: $scope.filter.carrier,
                        areacode: $scope.filter.areacode,
                        city: $scope.filter.city
                    });

                    $scope.neighborhoods.$promise.then(function(result) {
                        $scope.neighborhoods = result;
                        $scope.updateCount();
                    });
                }
            }

            $scope.updateCount = function() {

                var p_count = 0;

                for(var p in $scope.filter) {
                    if ($scope.filter[p]) {
                        p_count ++;
                    }
                }

                if (p_count <= 0) return;
                
                $scope.counting = true;
                $scope.updating = true;

                var params = jQuery.param($scope.filter);

                $http
                    .get('http://10.46.80.80:8080/filter/person/count/?' + params)
                    .then(
                        function(response) {
                            $scope.count = response.data.count;
                        },
                        function(response) {
                            console.log(response);
                        }
                    )
                    .finally(
                        function() {
                            $scope.counting = false;
                            $scope.updating = false;
                        }
                    );
            }

            $scope.$watch('filter.nature', $scope.updateStates, true);
            $scope.$watch('filter.state', $scope.updateCarriers);
            $scope.$watch('filter.carrier', $scope.updateAreacodes);
            $scope.$watch('filter.areacode', $scope.updateCities);
            $scope.$watch('filter.city', $scope.updateNeighborhoods, true);
            $scope.$watch('filter.neighborhood', $scope.updateCount, true);

        }
    ])
    .filter('nature', function() {
        return function(code) {
            var nature = 'Todos';
            if (code == 'L') {
                nature = 'Jurídica';
            }
            else if (code == 'P') {
                nature = 'Física';
            }

            return nature;
        }
    })
    .filter('cpf', function() {
        return function(item) {
            return item.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g, "\$1.\$2.\$3\-\$4");
        }
    })
    .filter('cnpj', function() {
        return function(item) {
            return item.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/g, "\$1.\$2.\$3\/\$4\-\$5");
        }
    })
    .filter("brl", ["numberFilter", function(numberFilter) {
        function isNumeric(value) {
            return (!isNaN(parseFloat(value)) && isFinite(value));
        }

        return function(inputNumber) {
            if (isNumeric(inputNumber)) {
                // Default values for the optional arguments
                var currencySymbol = "";
                var decimalSeparator = ",";
                var thousandsSeparator = ".";
                var decimalDigits = 2;

                if (decimalDigits < 0) decimalDigits = 0;

                // Format the input number through the number filter
                // The resulting number will have "," as a thousands separator
                // and "." as a decimal separator.
                var formattedNumber = numberFilter(inputNumber, decimalDigits);

                // Extract the integral and the decimal parts
                var numberParts = formattedNumber.split(".");

                // Replace the "," symbol in the integral part
                // with the specified thousands separator.
                numberParts[0] = numberParts[0].split(",").join(thousandsSeparator);

                // Compose the final result
                var result = currencySymbol + numberParts[0];

                if (numberParts.length == 2) {
                    result += decimalSeparator + numberParts[1];
                }

                return result;
            } else {
                return inputNumber;
            }
        };
    }]);

'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:AccountCtrl
 * @description
 * # AccountCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('CorporationCtrl', ['$rootScope', '$scope', 'toastr', 'Corporation', function($rootScope, $scope, toastr, Corporation) {
        $scope.page = {
            title: $rootScope.globals.currentUser.account.corporation.name
        };

        $scope.corporation = Corporation.get({id:$rootScope.globals.currentUser.account.corporation.id});

        $scope.onSubmit = function() {
        	var data = {name:  $scope.corporation.name, document: $scope.corporation.document }
        	Corporation
        		.update({id:$rootScope.globals.currentUser.account.corporation.id}, data)
        		.$promise.then(
        			function(data) {
        				toastr.success('Sucesso!');
        			}, 
        			function(error) {
        				if(error.status == 401) {
        					//
        				}
        			}
    			);
        };

    }]);
'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:PagesLoginCtrl
 * @description
 * # PagesLoginCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('LoginCtrl', ['$rootScope', '$window', '$location', '$scope', '$state', '$http', 'jwtHelper', 'AuthService', function($rootScope, $window, $location, $scope, $state, $http, jwtHelper, AuthService) {
        $scope.credentials = {};
        $scope.error = null;

        $scope.onSuccess = function(response) {
            AuthService.SetCredentials(response.data);

            var origin = $location.search().origin;

            if (typeof origin !== 'undefined' && origin) {
                $window.location = '#' + decodeURIComponent(origin);
            } else {
                $window.location = '#/app/dashboard/';
            }
        };

        $scope.onError = function(response) {
            if (response.status == 400) {
                $scope.error = response.data.non_field_errors[0];
            }
        };

        $scope.login = function() {
            $scope.credentials.token = AuthService.Login($scope.credentials.username, $scope.credentials.password, $scope.onSuccess, $scope.onError);
        };
    }]);

'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:PagesForgotPasswordCtrl
 * @description
 * # PagesForgotPasswordCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('ForgotPasswordCtrl', ["$state", "$scope", "$location", function($state, $scope, $location) {
        $scope.credentials = {};
        $scope.error = null;

        $scope.onSuccess = function(response) {
            //
        };

        $scope.onError = function(response) {
            if (response.status == 400) {
                $scope.error = response.data.non_field_errors[0];
            }
        };

        $scope.recover = function() {
            $location.path('/core/forgotpass/success');

        };
    }])
    .controller('ForgotPasswordSuccessCtrl', ["$state", "$scope", function($state, $scope) {
        
    }]);

'use strict';

app
    .factory('AuthService', AuthService);

AuthService.$inject = ['$injector', '$cookieStore', '$rootScope', '$timeout', 'jwtHelper'];

function AuthService($injector, $cookieStore, $rootScope, $timeout, jwtHelper) {
    var service = {};


    service.Login = Login;
    service.SetCredentials = SetCredentials;
    service.ClearCredentials = ClearCredentials;
    service.RefreshToken = RefreshToken;

    return service;

    function Login(username, password, success_callback, error_callback) {

        var data = {
            'username': username,
            'password': password
        };

        $injector.get("$http")
            .post('http://10.46.80.80:8080/api-token-auth/', data)
            .then(
                function(response) {
                    success_callback(response);
                },
                function(response) {
                    error_callback(response)
                }
            );
    }

    function RefreshToken(token, success_callback, error_callback) {

        $injector.get("$http")
            .post('http://10.46.80.80:8080/api-token-refresh/', {
                token: token
            })
            .then(
                function(response) {
                    service.SetCredentials(response.data);
                    success_callback(response);
                },
                function(response) {
                    service.ClearCredentials();
                    error_callback(response)
                }
            );
    }

    function SetCredentials(authdata) {

        var currentUser = authdata.user;
        currentUser.token = authdata.token;

        $rootScope.globals = {
            currentUser: currentUser
        };

        $injector.get("$http").defaults.headers.common['Authorization'] = 'JWT ' + authdata.token; // jshint ignore:line
        $cookieStore.put('globals', $rootScope.globals);
    }

    function ClearCredentials() {
        $rootScope.globals = {};
        $cookieStore.remove('globals');
        $injector.get("$http").defaults.headers.common.Authorization = 'JWT';
    }
}

app
    .factory('RefreshAuthTokenInterceptor', RefreshAuthTokenInterceptor)
    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.interceptors.push('RefreshAuthTokenInterceptor');
    }]);

RefreshAuthTokenInterceptor.$inject = ['$rootScope', '$q', 'jwtHelper', 'AuthService'];

function RefreshAuthTokenInterceptor($rootScope, $q, jwtHelper, AuthService) {

    var requestInterceptor = {

        request: function(config) {


            var deferred = $q.defer();

            var is_auth_request = (config.url.indexOf('/api-token') > -1);


            if (!is_auth_request && $rootScope.globals.currentUser && $rootScope.globals.currentUser.token) {

                var exp = moment(jwtHelper.getTokenExpirationDate($rootScope.globals.currentUser.token));
                var now = moment(new Date());

                if (exp.diff(now, 'minutes') <= 2) {

                    console.log('token about to expire... refreshing');
                    
                    AuthService.RefreshToken(
                        $rootScope.globals.currentUser.token,
                        function(response) {
                            deferred.resolve(config);
                        },
                        function(response) {
                            deferred.resolve(config);
                        }
                    );
                } else {
                    deferred.resolve(config);
                }


            } else {
                deferred.resolve(config);
            }


            return deferred.promise;
        }
    };

    return requestInterceptor;
}

'use strict';

app
    .factory('State', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/state/'
        );
    }])
    .factory('Carrier', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/carrier/'
        );
    }])
    .factory('Areacode', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/areacode/'
        );
    }])
    .factory('City', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/city/'
        );
    }])
    .factory('Neighborhood', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/neighborhood/'
        );
    }]);


'use strict';

app
    .factory('Person', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/person/:id', 
            { id: '@id'}, 
            {
                query : {
                    method: 'GET', 
                    isArray: true, 
                    transformResponse : function(data, headers) {
                        data = JSON.parse(data);
                        headers()['count'] = data.count;
                        headers()['next'] = data.next;
                        headers()['previous'] = data.previous;
                        return data.results;
                    }
                }
            }
        );
    }]);


'use strict';

app
    .factory('Corporation', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/account/corporation/:id/', 
            { id: '@id'},
            {
		        'update': { method:'PUT' }
		    }
        );
    }]);


'use strict';

app
    .factory('User', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/user/:id', 
            { id: '@id'}
        );
    }]);


'use strict';

app
    .factory('Cart', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/commerce/cart/:id/',
            { id: '@id'},
            {'query': {method: 'GET', isArray: false }}
        );
    }])
    .factory('Criteria', ["$resource", function($resource){
        return $resource(
            'http://10.46.80.80:8080/commerce/cart/checkout/criteria/:id/',
            { id: '@id'}
        );
    }]);


'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:collapseSidebarSm
 * @description
 * # collapseSidebarSm
 */
app
  .directive('collapseSidebar', ["$rootScope", function ($rootScope) {
    return {
      restrict: 'A',
      link: function postLink(scope, element) {

        var app = angular.element('.appWrapper'),
            $window = angular.element(window),
            width = $window.width();

        var removeRipple = function() {
          angular.element('#sidebar').find('.ink').remove();
        };

        var collapse = function() {

          width = $window.width();

          if (width < 992) {
            app.addClass('sidebar-sm');
          } else {
            app.removeClass('sidebar-sm sidebar-xs');
          }

          if (width < 768) {
            app.removeClass('sidebar-sm').addClass('sidebar-xs');
          } else if (width > 992){
            app.removeClass('sidebar-sm sidebar-xs');
          } else {
            app.removeClass('sidebar-xs').addClass('sidebar-sm');
          }

          if (app.hasClass('sidebar-sm-forced')) {
            app.addClass('sidebar-sm');
          }

          if (app.hasClass('sidebar-xs-forced')) {
            app.addClass('sidebar-xs');
          }

        };

        collapse();

        $window.resize(function() {
          if(width !== $window.width()) {
            var t;
            clearTimeout(t);
            t = setTimeout(collapse, 300);
            removeRipple();
          }
        });

        element.on('click', function(e) {
          if (app.hasClass('sidebar-sm')) {
            app.removeClass('sidebar-sm').addClass('sidebar-xs');
          }
          else if (app.hasClass('sidebar-xs')) {
            app.removeClass('sidebar-xs');
          }
          else {
            app.addClass('sidebar-sm');
          }

          app.removeClass('sidebar-sm-forced sidebar-xs-forced');
          app.parent().removeClass('sidebar-sm sidebar-xs');
          removeRipple();
          e.preventDefault();
        });

      }
    };
  }]);

'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:ripple
 * @description
 * # ripple
 */
app
  .directive('ripple', function () {
    return {
      restrict: 'A',
      link: function(scope, element) {
        var parent, ink, d, x, y;

        angular.element(element).find('>li>a').click(function(e){
          parent = angular.element(this).parent();

          if(parent.find('.ink').length === 0) {
            parent.prepend('<span class="ink"></span>');
          }

          ink = parent.find('.ink');
          //incase of quick double clicks stop the previous animation
          ink.removeClass('animate');

          //set size of .ink
          if(!ink.height() && !ink.width())
          {
            //use parent's width or height whichever is larger for the diameter to make a circle which can cover the entire element.
            d = Math.max(parent.outerWidth(), parent.outerHeight());
            ink.css({height: d, width: d});
          }

          //get click coordinates
          //logic = click coordinates relative to page - parent's position relative to page - half of self height/width to make it controllable from the center;
          x = e.pageX - parent.offset().left - ink.width()/2;
          y = e.pageY - parent.offset().top - ink.height()/2;

          //set the position and add class .animate
          ink.css({top: y+'px', left: x+'px'}).addClass('animate');

          setTimeout(function(){
            angular.element('.ink').remove();
          }, 600);
        });
      }
    };
  });

'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:NavCtrl
 * @description
 * # NavCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('NavCtrl', ["$scope", function ($scope) {
    $scope.oneAtATime = false;

    $scope.status = {
      isFirstOpen: true,
      isSecondOpen: true,
      isThirdOpen: true
    };

  }]);

'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:DaterangepickerCtrl
 * @description
 * # DaterangepickerCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('DaterangepickerCtrl', ["$scope", "$moment", function ($scope, $moment) {
    $scope.startDate = $moment().subtract(1, 'days').format('MMMM D, YYYY');
    $scope.endDate = $moment().add(31, 'days').format('MMMM D, YYYY');
    $scope.rangeOptions = {
      ranges: {
        Today: [$moment(), $moment()],
        Yesterday: [$moment().subtract(1, 'days'), $moment().subtract(1, 'days')],
        'Last 7 Days': [$moment().subtract(6, 'days'), $moment()],
        'Last 30 Days': [$moment().subtract(29, 'days'), $moment()],
        'This Month': [$moment().startOf('month'), $moment().endOf('month')],
        'Last Month': [$moment().subtract(1, 'month').startOf('month'), $moment().subtract(1, 'month').endOf('month')]
      },
      opens: 'left',
      startDate: $moment().subtract(29, 'days'),
      endDate: $moment(),
      parentEl: '#content'
    };
  }]);

'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:daterangepicker
 * @description
 * # daterangepicker
 */
app
  .directive('daterangepicker', function() {
    return {
      restrict: 'A',
      scope: {
        options: '=daterangepicker',
        start: '=dateBegin',
        end: '=dateEnd'
      },
      link: function(scope, element) {
        element.daterangepicker(scope.options, function(start, end) {
          scope.start = start.format('MMMM D, YYYY');
          scope.end = end.format('MMMM D, YYYY');
          scope.$apply();
        });
      }
    };
  });


'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:UiWidgetsCtrl
 * @description
 * # UiWidgetsCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('WidgetsCtrl', ["$scope", function ($scope) {
    $scope.page = {
      title: 'Widgets',
      subtitle: ''
    };
  }])

  .controller('TodoWidgetCtrl', ["$scope", function($scope) {
    $scope.todos = [{
      text: 'Release update',
      completed: false
    },{
      text: 'Make a backup',
      completed: false
    },{
      text: 'Send e-mail to Ici',
      completed: true
    },{
      text: 'Buy tickets',
      completed: false
    },{
      text: 'Resolve issues',
      completed: false
    },{
      text: 'Compile new version',
      completed: false
    }];

    var todos = $scope.todos;

    $scope.addTodo = function() {
      $scope.todos.push({
        text: $scope.todo,
        completed: false
      });
      $scope.todo = '';
    };

    $scope.removeTodo = function(todo) {
      todos.splice(todos.indexOf(todo), 1);
    };

    $scope.editTodo = function(todo) {
      $scope.editedTodo = todo;
      // Clone the original todo to restore it on demand.
      $scope.originalTodo = angular.extend({}, todo);
    };

    $scope.doneEditing = function(todo) {
      $scope.editedTodo = null;

      todo.text = todo.text.trim();

      if (!todo.text) {
        $scope.removeTodo(todo);
      }
    };

    $scope.revertEditing = function(todo) {
      todos[todos.indexOf(todo)] = $scope.originalTodo;
      $scope.doneEditing($scope.originalTodo);
    };

  }])

  .controller('CalendarWidgetCtrl', ["$scope", function ($scope) {

    $scope.today = function() {
      $scope.dt = new Date();
    };

    $scope.today();

    $scope.clear = function () {
      $scope.dt = null;
    };

    // Disable weekend selection
    $scope.disabled = function(date, mode) {
      return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
    };

    $scope.toggleMin = function() {
      $scope.minDate = $scope.minDate ? null : new Date();
    };
    $scope.toggleMin();

    $scope.open = function($event) {
      $event.preventDefault();
      $event.stopPropagation();

      $scope.opened = true;
    };

    $scope.dateOptions = {
      formatYear: 'yy',
      startingDay: 1,
      'class': 'datepicker'
    };

    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[0];
  }])

  .controller('MessageWidgetCtrl', ["$scope", function($scope){
    $scope.availableRecipients = ['RLake@nec.gov','RBastian@lacus.io','VMonroe@orci.ly','YMckenzie@mattis.gov','VMcmyne@molestie.org','BKliban@aliquam.gov','HHellems@tincidunt.org','KAngell@sollicitudin.ly'];
    $scope.recipients = {};
    $scope.recipients.emails = ['RLake@nec.gov','VMonroe@orci.ly'];

    $scope.messageContent = '<h2>Try me!</h2><p>textAngular is a super cool WYSIWYG Text Editor directive for AngularJS</p><p><b>Code at GitHub:</b> <a href="https://github.com/fraywing/textAngular">Here</a> </p>';
  }])

  .controller('AppointmentsWidgetCtrl', ["$scope", function($scope){
    $scope.date = new Date();
  }]);
