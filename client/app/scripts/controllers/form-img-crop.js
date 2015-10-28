'use strict';

/**
 * @ngdoc function
 * @name DATAPROJECT.controller:FormImgCropCtrl
 * @description
 * # FormImgCropCtrl
 * Controller of the DATAPROJECT
 */
app
  .controller('FormImgCropCtrl', function ($scope) {
    $scope.myImage='';
    $scope.myCroppedImage='';
    $scope.cropType='circle';

    var handleFileSelect=function(evt) {
      var file=evt.currentTarget.files[0];
      var reader = new FileReader();
      reader.onload = function (evt) {
        $scope.$apply(function($scope){
          $scope.myImage=evt.target.result;
        });
      };
      reader.readAsDataURL(file);
    };
    angular.element(document.querySelector('#fileInput')).on('change',handleFileSelect);
  });
