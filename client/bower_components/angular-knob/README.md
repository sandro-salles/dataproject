Angular jQuery Knob
===================

A angular directive of [jQuery Knob](https://github.com/aterrien/jQuery-Knob/blob/master/js/jquery.knob.js)

jQuery Knob is a

* canvas based ; no png or jpg sprites.
* touch, mouse and mousewheel, keyboard events implemented.
* downward compatible ; overloads an input element.

## Install

```
bower install angular-knob --save
```

## Example

```
angular.module('knobApp', ['ui.knob']);

angular.module('knobApp')
  .controller('exampleCtrl', ['$scope', function($scope){

    $scope.data = 30;

    $scope.max = 200;

    $scope.knobOptions = {
      'width':100,
      'displayInput': false
    };

  }]);
```

```
<body ng-app='knobApp'>
  <div ng-controller="exampleCtrl">
      <knob knob-data="data" knob-options="knobOptions"></knob>
      <knob knob-data="data" knob-max='max' knob-options="knobOptions"></knob>
  </div>
</body>
```

## Options

Behaviors :

* min : min value | default=0.
* max : max value | default=100.
*  step : step size | default=1.
*  angleOffset : starting angle in degrees | default=0.
* angleArc : arc size in degrees | default=360.
* stopper : stop at min & max on keydown/mousewheel | default=true.
* readOnly : disable input and events | default=false.

UI :

* cursor : display mode "cursor", cursor size could be changed passing a numeric value to the option, * default width is used when passing boolean value "true" | default=gauge.
* thickness : gauge thickness.
* lineCap : gauge stroke endings. | default=butt, round=rounded line endings
* width : dial width.
* displayInput : default=true | false=hide input.
* displayPrevious : default=false | true=displays the previous value with transparency.
* fgColor : foreground color.
* inputColor : input value (number) color.
* font : font family.
* fontWeight : font weight.
* bgColor : background color.

## Supported browser

Tested on Chrome, Safari, Firefox, IE 9.0.
