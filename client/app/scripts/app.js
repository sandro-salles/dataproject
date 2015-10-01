/**
 * DATAPROJECT - Responsive Admin Theme
 *
 */
(function () {
    angular.module('DATAPROJECT', [
        'ui.router',                    // Routing
        'oc.lazyLoad',                  // ocLazyLoad
        'ui.bootstrap',                 // Ui Bootstrap
    ])
})();

// Other libraries are loaded dynamically in the config.js file using the library ocLazyLoad